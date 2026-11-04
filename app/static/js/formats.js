"use strict";

window.AppFormat = (() => {
  const moneyDigits = value => {
    const raw = value.trim().replace(/\s*đ$/, "");
    return /^(?:[0-9]+|[0-9]{1,3}(?:\.[0-9]{3})+)$/.test(raw) ? raw.replaceAll(".", "") : raw === "" ? "" : null;
  };
  const money = value => `${BigInt(value).toLocaleString("vi-VN")} đ`;
  const isoDate = value => {
    const match = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(value);
    if (!match) return null;
    const [, day, month, year] = match;
    const date = new Date(`${year}-${month}-${day}T00:00:00Z`);
    return Number(year) >= 1 && !Number.isNaN(+date) && date.getUTCFullYear() === +year && date.getUTCMonth() + 1 === +month && date.getUTCDate() === +day ? `${year}-${month}-${day}` : null;
  };
  function enhance() {
    document.querySelectorAll("input[data-money]:not([data-format-bound])").forEach(input => {
      input.dataset.formatBound = "1";
      const update = (editing = false) => {
        const before = input.value;
        const position = input.selectionStart ?? before.length;
        const digitPosition = before.slice(0, position).replace(/\D/g, "").length;
        let raw = moneyDigits(before);
        // While editing an already grouped value, regroup the intermediate digits.
        if (editing && raw === null && /^[0-9.]+(?:\s*đ)?$/.test(before)) raw = before.replace(/\D/g, "");
        const maximum = BigInt(input.getAttribute("max") || "9223372036854775807");
        const valid = raw !== null && (raw === "" || (raw.length <= 19 && BigInt(raw) <= maximum));
        input.setCustomValidity(valid ? "" : "Nhập số tiền nguyên trong giới hạn cho phép, ví dụ 1.000.000 đ.");
        if (valid && raw !== "") {
          input.value = money(raw);
          if (editing && document.activeElement === input) {
            let count = 0, caret = 0;
            while (caret < input.value.length && count < digitPosition) {
              if (/\d/.test(input.value[caret])) count++;
              caret++;
            }
            input.setSelectionRange(caret, caret);
          }
        }
      };
      input.addEventListener("input", () => update(true));
      input.addEventListener("blur", () => update());
      input.addEventListener("paste", event => {
        const text = event.clipboardData.getData("text");
        if (moneyDigits(text) === null) {
          event.preventDefault();
          input.setCustomValidity("Số tiền dán vào không hợp lệ; dùng dạng 1.000.000 đ.");
          input.reportValidity();
        }
      });
      update();
    });
    document.querySelectorAll("input[data-date]:not([data-format-bound])").forEach(input => {
      input.dataset.formatBound = "1";
      const validate = () => {
        const iso = isoDate(input.value);
        const valid = input.value === "" || (iso && (!input.max || iso <= input.max) && (!input.min || iso >= input.min));
        input.setCustomValidity(valid ? "" : "Nhập ngày hợp lệ dạng dd/mm/yyyy, trong khoảng cho phép.");
      };
      input.addEventListener("input", () => {
        const digitPosition = input.value.slice(0, input.selectionStart ?? input.value.length).replace(/\D/g, "").length;
        if (/^[0-9/]*$/.test(input.value) && input.value.replaceAll("/", "").length <= 8) {
          const raw = input.value.replaceAll("/", "");
          input.value = [raw.slice(0, 2), raw.slice(2, 4), raw.slice(4)].filter(Boolean).join("/");
          let count = 0, caret = 0;
          while (caret < input.value.length && count < digitPosition) {
            if (/\d/.test(input.value[caret])) count++;
            caret++;
          }
          input.setSelectionRange(caret, caret);
        }
        validate();
      });
      input.addEventListener("blur", validate);
      validate();
    });
  }
  return { moneyDigits, money, isoDate, enhance };
})();
