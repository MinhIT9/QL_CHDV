"use strict";

function enhancePage() {
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
    meterForm.querySelectorAll(".reading-row").forEach((row) => {
      const start = row.querySelector(".start-value");
      const end = row.querySelector(".end-value");
      const output = row.querySelector(".consumption");
      if (!start || !end || !output) return;
      const startRaw = start.dataset.value ?? start.value;
      const endRaw = end.value;
      end.setCustomValidity("");
      if (start.tagName === "INPUT") start.required = endRaw !== "";
      if (startRaw === "" || endRaw === "") { output.textContent = "—"; return; }
      const consumption = Number(endRaw) - Number(startRaw);
      if (consumption < 0) {
        end.setCustomValidity("Chỉ số cuối không được nhỏ hơn chỉ số đầu.");
        output.textContent = "Không hợp lệ";
      } else {
        output.textContent = consumption.toLocaleString("vi-VN");
        total += consumption;
      }
    });
    document.querySelector("#draft-total").textContent = `${total.toLocaleString("vi-VN")} kWh`;
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
