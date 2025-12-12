export const resizeImage = (file, maxWidth = 1280, maxHeight = 1280, quality = 0.8) => {
  return new Promise((resolve, reject) => {
    try {
      const img = new Image()
      img.onload = () => {
        let { width, height } = img
        const ratio = Math.min(maxWidth / width, maxHeight / height, 1)
        const targetW = Math.round(width * ratio)
        const targetH = Math.round(height * ratio)
        const canvas = document.createElement('canvas')
        canvas.width = targetW
        canvas.height = targetH
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0, targetW, targetH)
        canvas.toBlob(
          (blob) => {
            if (!blob) return reject(new Error('Image compression failed'))
            const ext = (file.name && file.name.split('.').pop()) || 'jpg'
            const name = file.name ? file.name.replace(/\.[^.]+$/, '') : 'image'
            const out = new File([blob], `${name}_compressed.${ext}`, { type: blob.type })
            resolve(out)
          },
          'image/jpeg',
          quality
        )
      }
      img.onerror = () => reject(new Error('Image load error'))
      const reader = new FileReader()
      reader.onload = () => {
        img.src = reader.result
      }
      reader.onerror = () => reject(new Error('File read error'))
      reader.readAsDataURL(file)
    } catch (e) {
      reject(e)
    }
  })
}
