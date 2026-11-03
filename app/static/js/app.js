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
const billRoom = document.querySelector("#bill-room");
if (billRoom && !billRoom.dataset.bound) {
  billRoom.dataset.bound = "true";
  billRoom.addEventListener("change", () => { document.querySelector("#bill-create").href = billRoom.value; });
}
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
          if (amount) amount.textContent = `${cost.toLocaleString("vi-VN")} đ`;
        }
      }
    });
    document.querySelector("#draft-total").textContent = `${total.toLocaleString("vi-VN")} kWh`;
    const draftMoney = document.querySelector("#draft-money");
    if (draftMoney) draftMoney.textContent = missingPrice ? "Chưa đủ đơn giá" : `${money.toLocaleString("vi-VN")} đ`;
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
