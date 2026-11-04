"use strict";
document.querySelector("#print-receipt")?.addEventListener("click", () => window.print());

const sheet = document.querySelector('.receipt-sheet');
const saveButton = document.querySelector('#save-receipt');
const dialog = document.querySelector('#receipt-image-dialog');
const preview = document.querySelector('#receipt-image-preview');
const download = document.querySelector('#download-receipt-image');
const shareButton = document.querySelector('#share-receipt-image');
const message = document.querySelector('#receipt-export-message');
const shareMessage = document.querySelector('#receipt-share-message');
let imageUrl = null;
let imageFile = null;

function fitTotal(container) {
  const amount = container.querySelector('.receipt-total b');
  amount.style.removeProperty('font-size');
  let size = parseFloat(amount.ownerDocument.defaultView.getComputedStyle(amount).fontSize);
  while (amount.scrollWidth > amount.clientWidth && size > 8) {
    amount.style.fontSize = `${--size}px`;
  }
}

fitTotal(sheet);
window.addEventListener('resize', () => fitTotal(sheet));
document.querySelector('#close-receipt-image').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => saveButton.focus());

saveButton.addEventListener('click', async () => {
  if (saveButton.disabled) return;
  saveButton.disabled = true;
  saveButton.textContent = 'Đang tạo ảnh…';
  message.textContent = '';
  shareMessage.textContent = '';
  try {
    await document.fonts.ready;
    const images = [...sheet.querySelectorAll('img')];
    await Promise.all(images.map(image => image.decode()));
    const imageData = images.map(image => {
      const pixels = document.createElement('canvas');
      pixels.width = image.naturalWidth;
      pixels.height = image.naturalHeight;
      pixels.getContext('2d').drawImage(image, 0, 0);
      const data = pixels.toDataURL('image/png');
      pixels.width = pixels.height = 0;
      return data;
    });
    const canvas = await html2canvas(sheet, {
      scale: 2, backgroundColor: '#ffffff', logging: false, windowWidth: 1000,
      onclone: clone => {
        const copy = clone.querySelector('.receipt-sheet');
        copy.style.width = '800px';
        copy.style.maxWidth = '800px';
        copy.style.margin = '0';
        copy.style.boxShadow = 'none';
        copy.querySelectorAll('img').forEach((image, index) => { image.src = imageData[index]; });
        fitTotal(copy);
      },
    });
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
    canvas.width = canvas.height = 0;
    if (!blob) throw new Error('Không tạo được ảnh. Vui lòng thử lại.');
    if (imageUrl) URL.revokeObjectURL(imageUrl);
    imageUrl = URL.createObjectURL(blob);
    imageFile = new File([blob], sheet.dataset.imageName, { type: 'image/png' });
    preview.src = imageUrl;
    download.href = imageUrl;
    download.download = imageFile.name;
    shareButton.hidden = !(navigator.share && navigator.canShare?.({ files: [imageFile] }));
    dialog.showModal();
  } catch {
    message.textContent = 'Không tạo được ảnh phiếu. Kiểm tra ảnh QR đã tải đầy đủ rồi thử lại; bạn vẫn có thể dùng In phiếu.';
  } finally {
    saveButton.disabled = false;
    saveButton.textContent = 'Lưu ảnh phiếu';
  }
});

shareButton.addEventListener('click', async () => {
  if (!imageFile || shareButton.disabled) return;
  shareButton.disabled = true;
  shareMessage.textContent = '';
  try {
    await navigator.share({ files: [imageFile] });
  } catch (error) {
    if (error.name !== 'AbortError') shareMessage.textContent = 'Chưa chia sẻ được. Bạn có thể tải ảnh hoặc nhấn giữ ảnh xem trước để lưu.';
  } finally {
    shareButton.disabled = false;
  }
});

window.addEventListener('pagehide', () => {
  dialog.close();
  if (imageUrl) URL.revokeObjectURL(imageUrl);
  imageUrl = imageFile = null;
  preview.removeAttribute('src');
  download.removeAttribute('href');
});
