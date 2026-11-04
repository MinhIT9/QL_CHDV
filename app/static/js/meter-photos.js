"use strict";

(() => {
  const csrf = () => document.querySelector("input[name='csrf_token']")?.value || "";
  const message = (widget, text) => { widget.querySelector(".photo-message").textContent = text; };
  const thumbnail = (url) => {
    const link = document.createElement("a");
    link.href = url;
    link.className = "photo-open";
    link.setAttribute("hx-boost", "false");
    const img = document.createElement("img");
    Object.assign(img, { src: url, alt: "Ảnh công tơ", width: 72, height: 72, loading: "lazy", className: "photo-thumb rounded border" });
    link.append(img);
    return link;
  };
  const clear = (widget) => {
    if (widget.previewURL) URL.revokeObjectURL(widget.previewURL);
    widget.previewURL = null;
    widget.uploadToken = null;
    widget.querySelector("input[type=file]").value = "";
    widget.querySelector(".photo-preview").replaceChildren();
    widget.querySelectorAll(".photo-save,.photo-clear").forEach(button => { button.hidden = true; });
  };
  const select = (widget, file) => {
    if (!file || widget.busy) return;
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type) || file.size > 10 * 1024 * 1024) {
      clear(widget);
      message(widget, "Chọn JPEG, PNG hoặc WebP, tối đa 10 MB.");
      return;
    }
    clear(widget);
    const transfer = new DataTransfer();
    transfer.items.add(file);
    widget.querySelector("input[type=file]").files = transfer.files;
    widget.uploadToken = crypto.randomUUID().replaceAll("-", "");
    widget.previewURL = URL.createObjectURL(file);
    widget.querySelector(".photo-preview").append(thumbnail(widget.previewURL));
    widget.querySelectorAll(".photo-save,.photo-clear").forEach(button => { button.hidden = false; });
    message(widget, "Chưa tải lên · bấm Lưu ảnh hoặc Lưu chỉ số.");
  };
  const request = (url, data, header, progress) => new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader(header, "1");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.timeout = 120000;
    xhr.upload.onprogress = event => progress(event.lengthComputable ? Math.round(event.loaded * 100 / event.total) : null);
    xhr.onload = () => {
      if (xhr.status === 413) { reject(new Error("Dữ liệu vượt giới hạn upload. Hãy chọn ảnh nhỏ hơn hoặc lưu ít phòng mỗi lần.")); return; }
      let result;
      try { result = JSON.parse(xhr.responseText); }
      catch { reject(new Error("Không nhận được kết quả. Phiên đăng nhập có thể đã hết; kiểm tra lại trước khi gửi tiếp.")); return; }
      if (xhr.status >= 200 && xhr.status < 300) resolve(result);
      else reject(new Error(result.error || `Không lưu được (${xhr.status}). Kiểm tra ảnh, kích thước hoặc phiên đăng nhập.`));
    };
    xhr.onerror = xhr.ontimeout = () => reject(new Error("Mất kết nối hoặc hết thời gian chờ. Kiểm tra kết quả trước khi gửi lại."));
    xhr.send(data);
  });
  const pending = (photo) => {
    if (photo.status === "ready") return thumbnail(photo.url);
    const span = document.createElement("span");
    span.className = `badge text-bg-${photo.status === "failed" ? "danger" : "secondary"}`;
    span.textContent = photo.status === "failed" ? "Xử lý lỗi · chọn lại ảnh để tải lại" : "Đã tải lên · đang xử lý…";
    if (photo.status === "pending") span.dataset.photoPending = photo.id;
    return span;
  };
  let polling = false;
  async function poll() {
    const nodes = [...document.querySelectorAll("[data-photo-pending]")].filter(node => !node.dataset.paused).slice(0, 100);
    if (polling || !nodes.length || document.hidden) return;
    polling = true;
    try {
      const ids = [...new Set(nodes.map(node => node.dataset.photoPending))];
      const response = await fetch(`/photos/status?ids=${ids.join(',')}`, { headers: { Accept: "application/json" } });
      if (!response.ok || !response.headers.get("Content-Type")?.includes("application/json")) throw new Error("status unavailable");
      const result = await response.json();
      for (const node of nodes) {
        const photo = result.photos.find(item => String(item.id) === node.dataset.photoPending);
        if (photo && photo.status !== "pending") node.replaceWith(pending(photo));
        else {
          node.dataset.pollCount = Number(node.dataset.pollCount || 0) + 1;
          if (Number(node.dataset.pollCount) >= 30) {
            node.dataset.paused = "1";
            node.textContent = "Ảnh vẫn đang chờ · bấm để kiểm tra lại";
            node.tabIndex = 0;
            node.setAttribute("role", "button");
          }
        }
      }
    } catch {
      for (const node of nodes) {
        node.dataset.paused = "1";
        node.textContent = "Chưa kiểm tra được ảnh · bấm để thử lại";
        node.tabIndex = 0;
        node.setAttribute("role", "button");
      }
    } finally { polling = false; }
  }
  setInterval(poll, 2000);
  document.addEventListener("click", event => {
    const retry = event.target.closest("[data-photo-pending][data-paused]");
    if (retry) { delete retry.dataset.paused; retry.dataset.pollCount = "0"; retry.textContent = "Đang kiểm tra…"; poll(); }
    const link = event.target.closest(".photo-open");
    if (!link || !window.bootstrap) return;
    event.preventDefault();
    const modal = document.querySelector("#meter-photo-modal");
    modal.querySelector("img").src = link.href;
    bootstrap.Modal.getOrCreateInstance(modal).show();
  });
  document.addEventListener("keydown", event => {
    if (["Enter", " "].includes(event.key) && event.target.matches("[data-photo-pending][data-paused]")) { event.preventDefault(); event.target.click(); }
  });
  window.addEventListener("beforeunload", event => {
    if ([...document.querySelectorAll(".meter-photo-widget")].some(widget => widget.busy || widget.querySelector("input[type=file]").files.length)) {
      event.preventDefault(); event.returnValue = "";
    }
  });
  document.addEventListener("htmx:beforeRequest", event => {
    if (!event.detail.elt.closest("a")) return;
    const dirty = [...document.querySelectorAll(".meter-photo-widget")].some(widget => widget.busy || widget.querySelector("input[type=file]").files.length);
    if (dirty && !window.confirm("Có ảnh chưa lưu hoặc đang tải. Bạn muốn rời trang?")) event.preventDefault();
  });
  document.addEventListener("htmx:beforeCleanupElement", event => {
    if (event.detail.elt.previewURL) URL.revokeObjectURL(event.detail.elt.previewURL);
  });
  window.enhanceMeterPhotos = () => {
    document.querySelectorAll(".meter-photo-widget:not([data-bound])").forEach(widget => {
      widget.dataset.bound = "1";
      const input = widget.querySelector("input[type=file]");
      input.addEventListener("change", () => select(widget, input.files[0]));
      const drop = widget.querySelector(".photo-drop");
      drop.addEventListener("keydown", event => { if (event.target === drop && ["Enter", " "].includes(event.key)) { event.preventDefault(); input.click(); } });
      drop.addEventListener("dragover", event => { event.preventDefault(); drop.classList.add("border-primary"); });
      drop.addEventListener("dragleave", () => drop.classList.remove("border-primary"));
      drop.addEventListener("drop", event => {
        event.preventDefault(); drop.classList.remove("border-primary");
        if (event.dataTransfer.files.length) select(widget, event.dataTransfer.files[0]);
        else message(widget, "Nguồn này không cung cấp file ảnh. Hãy lưu ảnh về máy rồi kéo vào.");
      });
      widget.querySelector(".photo-clear").addEventListener("click", () => { if (!widget.busy) { clear(widget); message(widget, ""); } });
      widget.querySelector(".photo-save")?.addEventListener("click", async () => {
        if (widget.busy || !input.files.length) return;
        widget.busy = true;
        input.disabled = true;
        const bar = widget.querySelector("progress");
        bar.hidden = false; bar.value = 0;
        const data = new FormData();
        data.append("photo", input.files[0]); data.append("csrf_token", csrf()); data.append("upload_token", widget.uploadToken);
        try {
          const result = await request(widget.dataset.uploadUrl, data, "X-Photo-Upload", value => {
            if (value === null) bar.removeAttribute("value"); else bar.value = value;
            message(widget, value === null ? "Đang tải…" : `Đang tải ${value}%${value === 100 ? ' · chờ máy chủ xác nhận' : ''}`);
          });
          const list = widget.querySelector(".saved-photos");
          if (!list.querySelector(".photo-open,[data-photo-pending]")) list.replaceChildren();
          list.append(pending(result.photo)); clear(widget); message(widget, "Đã nhận ảnh."); poll();
        } catch (error) { message(widget, error.message); }
        finally { widget.busy = false; input.disabled = false; bar.hidden = true; }
      });
    });
    const form = document.querySelector("#electricity-form");
    if (!form || form.dataset.photoBound) return;
    form.dataset.photoBound = "1";
    const feedback = document.createElement("div");
    feedback.className = "p-3 small"; feedback.setAttribute("role", "status");
    const bar = document.createElement("progress"); bar.max = 100; bar.hidden = true; bar.className = "w-100";
    form.append(bar, feedback);
    form.addEventListener("submit", async event => {
      event.preventDefault();
      if (form.dataset.saving) return;
      const rows = [...form.querySelectorAll(".reading-row")].filter(row => row.querySelector(".end-value")?.value !== undefined && row.querySelector(".end-value").value !== "");
      if (!rows.length) { feedback.textContent = "Nhập chỉ số cuối cho ít nhất một phòng; ảnh phòng đã chốt dùng nút Lưu ảnh."; return; }
      if (rows.some(row => row.querySelector(".meter-photo-widget")?.busy)) return;
      const data = new FormData(form);
      form.querySelectorAll(".meter-photo-widget input[type=file]").forEach(input => {
        if (!input.files.length || !rows.includes(input.closest(".reading-row"))) data.delete(input.name);
      });
      // Existing readings have their own explicit Save photo button.
      form.querySelectorAll(".meter-photo-widget[data-upload-url]:not([data-upload-url='']) input[type=file]").forEach(input => data.delete(input.name));
      form.dataset.saving = "1";
      const button = event.submitter;
      if (button) button.disabled = true;
      rows.forEach(row => { const widget = row.querySelector(".meter-photo-widget"); if (widget) widget.busy = true; });
      rows.forEach(row => row.querySelectorAll("input").forEach(input => { input.disabled = true; }));
      bar.hidden = false; bar.value = 0;
      try {
        const result = await request(form.action, data, "X-Meter-Save", value => {
          if (value === null) bar.removeAttribute("value"); else bar.value = value;
          feedback.textContent = value === null ? "Đang tải…" : `Đang tải ${value}% · chờ xác nhận lưu`;
        });
        const page = new DOMParser().parseFromString(result.html, "text/html");
        rows.forEach(row => {
          const fresh = page.querySelector(`.reading-row[data-room-id='${row.dataset.roomId}']`);
          if (fresh) { const widget = row.querySelector(".meter-photo-widget"); if (widget) clear(widget); row.replaceWith(fresh); }
        });
        const badge = document.querySelector(".section-heading .badge");
        if (badge) badge.textContent = page.querySelector(".section-heading .badge").textContent;
        feedback.textContent = "Đã lưu chỉ số. Ảnh đã nhận sẽ tự hiển thị sau khi xử lý.";
        window.enhanceMeterPhotos(); poll();
      } catch (error) { feedback.textContent = error.message; }
      finally {
        delete form.dataset.saving; bar.hidden = true;
        rows.forEach(row => { const widget = row.querySelector(".meter-photo-widget"); if (widget) widget.busy = false; });
        rows.forEach(row => row.querySelectorAll("input").forEach(input => { input.disabled = false; }));
        if (button) button.disabled = !form.querySelector(".end-value");
        form.dispatchEvent(new Event("input"));
      }
    });
    poll();
  };
})();
