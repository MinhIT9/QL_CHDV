"use strict";

function positionPaymentPanel(panel) {
  const anchor = document.querySelector(`button[popovertarget="${panel.id}"]`);
  if (!anchor) return;
  const rect = anchor.getBoundingClientRect();
  if (rect.bottom < 0 || rect.top > innerHeight || rect.right < 0 || rect.left > innerWidth) {
    panel.hidePopover();
    return;
  }
  const gap = 8, edge = 12;
  const height = panel.offsetHeight, width = panel.offsetWidth;
  const below = rect.bottom + gap;
  const top = below + height <= innerHeight - edge ? below : rect.top - height - gap;
  panel.style.left = `${Math.max(edge, Math.min(rect.right - width, innerWidth - width - edge))}px`;
  panel.style.top = `${Math.max(edge, Math.min(top, innerHeight - height - edge))}px`;
}

function repositionPaymentPanels() {
  document.querySelectorAll(".payment-panel:popover-open").forEach(positionPaymentPanel);
}
window.addEventListener("resize", repositionPaymentPanels);
window.addEventListener("scroll", repositionPaymentPanels, true);

function enhancePage() {
window.AppFormat.enhance();
window.enhanceMeterPhotos?.();
const amountForm = document.querySelector("#bill-amount-form");
if (amountForm && !amountForm.dataset.amountBound) {
  amountForm.dataset.amountBound = "1";
  const final = amountForm.elements.final_amount;
  const reason = amountForm.elements.adjustment_reason;
  let manual = final.value !== "";
  const money = window.AppFormat.money;
  const updateAmount = () => {
    const names = ["rent_price", "water_price", "service_price", "electricity_price", "people_count"];
    const raw = names.map(name => amountForm.elements[name].matches("[data-money]") ? window.AppFormat.moneyDigits(amountForm.elements[name].value) : amountForm.elements[name].value);
    if (!raw.every(value => /^\d+$/.test(value)) || !/^\d+$/.test(amountForm.dataset.consumption)) {
      amountForm.querySelector("#bill-computed-total").textContent = "Chưa đủ dữ liệu";
      return;
    }
    const [rent, water, service, electricity, people] = raw.map(BigInt);
    const computed = rent + water * people + service + electricity * BigInt(amountForm.dataset.consumption);
    amountForm.querySelector("#bill-computed-total").textContent = money(computed);
    if (!manual) final.value = money(computed);
    const finalRaw = window.AppFormat.moneyDigits(final.value);
    const valid = /^\d{1,19}$/.test(finalRaw) && BigInt(finalRaw) <= 9223372036854775807n;
    final.setCustomValidity(valid ? "" : "Số tiền thu cuối cùng phải là số nguyên không âm trong giới hạn cho phép.");
    const difference = valid ? BigInt(finalRaw) - computed : 0n;
    const priceChanged = amountForm.dataset.editing
      ? names.slice(0, 4).some((name, index) => BigInt(raw[index]) !== BigInt(amountForm.getAttribute(`data-original-${name.replaceAll('_', '-')}`))) || (valid && BigInt(finalRaw) !== BigInt(amountForm.dataset.originalTotal))
      : valid && difference !== 0n;
    reason.required = Boolean(priceChanged);
    reason.closest('[data-price-reason]').hidden = !priceChanged;
    amountForm.querySelector("#bill-adjustment").textContent = valid ? `Điều chỉnh: ${difference > 0n ? '+' : ''}${money(difference)}` : "";
  };
  final.addEventListener("input", () => { manual = final.value !== ""; updateAmount(); });
  amountForm.addEventListener("input", updateAmount);
  amountForm.querySelector("#bill-reset-total")?.addEventListener("click", () => { manual = false; updateAmount(); });
  updateAmount();
}
const sidebar = document.querySelector("#sidebar");
const sidebarToggle = document.querySelector(".sidebar-toggle");
if (sidebar && sidebarToggle && !sidebarToggle.dataset.bound) {
  sidebarToggle.dataset.bound = "true";
  const setSidebar = (collapsed) => {
    document.documentElement.classList.toggle("sidebar-collapsed", collapsed);
    sidebar.hidden = collapsed;
    sidebarToggle.setAttribute("aria-expanded", String(!collapsed));
    sidebarToggle.title = sidebarToggle.ariaLabel = collapsed ? "Hiện thanh điều hướng" : "Ẩn thanh điều hướng";
  };
  try { setSidebar(localStorage.getItem("chdv-sidebar-collapsed") === "true"); } catch { setSidebar(false); }
  sidebarToggle.addEventListener("click", () => {
    const collapsed = !sidebar.hidden;
    setSidebar(collapsed);
    try { localStorage.setItem("chdv-sidebar-collapsed", String(collapsed)); } catch { /* Storage may be disabled. */ }
    repositionPaymentPanels();
  });
}
document.querySelectorAll(".payment-panel[popover]:not([data-bound])").forEach((panel) => {
  panel.dataset.bound = "true";
  panel.addEventListener("beforetoggle", (event) => {
    if (event.newState === "open") panel.style.visibility = "hidden";
  });
  panel.addEventListener("toggle", (event) => {
    if (event.newState === "open") {
      positionPaymentPanel(panel);
      panel.style.visibility = "visible";
    }
  });
  panel.addEventListener("toggle", (event) => {
    if (event.target !== panel && panel.matches(":popover-open")) positionPaymentPanel(panel);
  }, true);
});
document.querySelectorAll("form").forEach((form) => form.setAttribute("hx-boost", "false"));
const status = document.querySelector("#room-status");
if (status && !status.dataset.bound) {
  status.dataset.bound = "true";
  const updateTenantFields = () => {
    const occupied = status.value === "occupied";
    document.querySelector("#tenant-fields").disabled = !occupied;
    document.querySelector("input[name='tenant_name']").required = occupied;
    const newTenant = document.querySelector("input[name='new_tenancy']");
    const hasCurrent = Boolean(document.querySelector("input[name='tenancy_id']").value);
    const isNew = !hasCurrent || Boolean(newTenant?.checked);
    document.querySelectorAll("[data-new-required]").forEach((input) => {
      input.required = occupied && isNew;
    });
    const moveOut = document.querySelector("input[name='move_out_date']");
    if (moveOut) {
      moveOut.required = !occupied || Boolean(newTenant?.checked);
      document.querySelector("#move-out-field").hidden = !moveOut.required;
      moveOut.disabled = !moveOut.required;
    }
  };
  status.addEventListener("change", updateTenantFields);
  document.querySelector("input[name='new_tenancy']")?.addEventListener("change", updateTenantFields);
  updateTenantFields();
}
document.querySelectorAll("form[data-confirm]:not([data-confirm-bound])").forEach((form) => {
  form.dataset.confirmBound = "true";
  form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});

const meterForm = document.querySelector("#electricity-form");
if (meterForm && !meterForm.dataset.bound) {
  meterForm.dataset.bound = "true";
  const updateConsumption = () => {
    let total = 0;
    let money = 0n;
    let missingPrice = false;
    meterForm.querySelectorAll(".reading-row").forEach((row) => {
      const start = row.querySelector(".start-value");
      const end = row.querySelector(".end-value");
      const output = row.querySelector(".consumption");
      const amount = row.querySelector(".reading-amount");
      if (!start || !end || !output) return;
      const startRaw = start.dataset.value ?? start.value;
      const endRaw = end.value;
      const photo = row.querySelector(".meter-photo");
      if (photo) photo.required = false;
      end.setCustomValidity("");
      if (start.tagName === "INPUT") start.required = endRaw !== "";
      if (amount) amount.textContent = "—";
      if (startRaw === "" || endRaw === "") { output.textContent = "—"; return; }
      const consumption = Number(endRaw) - Number(startRaw);
      if (consumption < 0 || !Number.isInteger(Number(startRaw)) || !Number.isInteger(Number(endRaw))) {
        end.setCustomValidity("Chỉ số phải là số nguyên; cuối không được nhỏ hơn đầu.");
        output.textContent = "Không hợp lệ";
      } else {
        output.textContent = consumption.toLocaleString("vi-VN");
        total += consumption;
        if (row.dataset.price === "") {
          missingPrice = true;
          if (amount) amount.textContent = "Chưa có giá";
        } else {
          const cost = BigInt(consumption) * BigInt(row.dataset.price);
          money += cost;
          if (amount) amount.textContent = window.AppFormat.money(cost);
        }
      }
    });
    document.querySelector("#draft-total").textContent = `${total.toLocaleString("vi-VN")} kWh`;
    const draftMoney = document.querySelector("#draft-money");
    if (draftMoney) draftMoney.textContent = missingPrice ? "Chưa đủ đơn giá" : window.AppFormat.money(money);
  };
  meterForm.addEventListener("input", updateConsumption);
  updateConsumption();
}

document.querySelectorAll("form[method='post']:not([data-submit-bound])").forEach((form) => {
  form.dataset.submitBound = "true";
  form.addEventListener("submit", (event) => {
    if (event.defaultPrevented) return;
    // Disabled submitters are omitted by browsers; preserve named actions (renewal preview/confirm).
    if (event.submitter?.name) {
      const action = document.createElement("input");
      action.type = "hidden";
      action.name = event.submitter.name;
      action.value = event.submitter.value;
      form.appendChild(action);
    }
    form.querySelectorAll("button[type='submit']").forEach((button) => {
      button.disabled = true;
      button.textContent = "Đang lưu…";
    });
  });
});
}
enhancePage();
document.addEventListener("htmx:load", enhancePage);
window.addEventListener("pageshow", (event) => { if (event.persisted) window.location.reload(); });
