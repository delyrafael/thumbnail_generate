import gradio as gr
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import os

class ProThumbnailRembg:
    def __init__(self):
        # Path font - Sesuaikan dengan OS Anda
        self.font_path = "C:/Windows/Fonts/arialbd.ttf" 
        if not os.path.exists(self.font_path):
            self.font_path = None # Akan fallback ke default jika tidak ketemu

    def remove_bg(self, image_array):
        """Menghapus background menggunakan library rembg"""
        # rembg menerima input PIL Image atau numpy array
        input_image = Image.fromarray(image_array)
        output_image = remove(input_image)
        return output_image

    def create_collage_bg(self, frames, target_size=(1280, 720)):
        """Membuat background grid 2x2 dari scene video"""
        bg = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
        h, w = target_size[1], target_size[0]
        grid_h, grid_w = h // 2, w // 2
        
        for i in range(min(4, len(frames))):
            frame = cv2.resize(frames[i], (grid_w, grid_h))
            # Tambahkan filter gelap agar teks menonjol (overlay 60% brightness)
            frame = cv2.addWeighted(frame, 0.4, np.zeros(frame.shape, frame.dtype), 0, 0)
            
            y_off = (i // 2) * grid_h
            x_off = (i % 2) * grid_w
            bg[y_off:y_off+grid_h, x_off:x_off+grid_w] = frame
        return bg

    def assemble(self, main_frame, all_frames, text):
        # 1. Buat Background Collage
        collage_bg_np = self.create_collage_bg([f[0] for f in all_frames])
        pil_bg = Image.fromarray(collage_bg_np).convert("RGBA")
        
        # 2. Hapus BG Subjek
        pil_subject = self.remove_bg(main_frame)
        
        # 3. Resize Subjek
        sub_w, sub_h = pil_subject.size
        ratio = 720 / sub_h
        new_size = (int(sub_w * ratio), 720)
        pil_subject = pil_subject.resize(new_size, Image.Resampling.LANCZOS)
        
        # 4. BUAT DROP SHADOW (Bayangan)
        # Membuat bayangan hitam transparan di belakang orang
        shadow = Image.new("RGBA", pil_bg.size, (0, 0, 0, 0))
        shadow_offset = (pil_bg.width - pil_subject.width - 15, 15) # Geser sedikit
        
        # Ambil alpha channel subjek untuk bayangan
        subject_mask = pil_subject.split()[3]
        black_shadow = Image.new("RGBA", pil_subject.size, (0, 0, 0, 150)) # Hitam transparan
        shadow.paste(black_shadow, shadow_offset, mask=subject_mask)
        
        # Gabungkan: Background -> Shadow -> Subjek
        pil_bg = Image.alpha_composite(pil_bg, shadow)
        pil_bg.alpha_composite(pil_subject, (pil_bg.width - pil_subject.width, 0))
        
        # 5. Tambahkan Headline
        draw = ImageDraw.Draw(pil_bg)
        try:
            font = ImageFont.truetype(self.font_path, 110) if self.font_path else ImageFont.load_default()
        except:
            font = ImageFont.load_default()
            
        text_pos = (60, 480)
        bbox = draw.textbbox(text_pos, text, font=font)
        # Box Merah khas YouTube Edukasi
        draw.rectangle([bbox[0]-20, bbox[1]-10, bbox[2]+20, bbox[3]+10], fill=(220, 20, 60))
        draw.text(text_pos, text, font=font, fill=(255, 255, 255))
        
        return np.array(pil_bg.convert("RGB"))

# Inisialisasi
creator = ProThumbnailRembg()
video_frames = []

def process_video(video):
    global video_frames
    if video is None: return None, "Upload video terlebih dahulu!"
    
    cap = cv2.VideoCapture(video)
    frames = []
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Ambil 8 frame untuk dipilih user
    for i in range(8):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i * (total/8)))
        ret, f = cap.read()
        if ret:
            frames.append((cv2.cvtColor(f, cv2.COLOR_BGR2RGB), i))
    cap.release()
    
    video_frames = frames
    return [f[0] for f in frames], "Video berhasil diproses! Silakan pilih frame subjek utama."

def generate(index, text):
    if not video_frames or index is None: 
        return None
    if not text: text = "HEADLINE DISINI"
    
    main_frame = video_frames[index][0]
    result = creator.assemble(main_frame, video_frames, text.upper())
    return result

# --- UI GRADIO ---
with gr.Blocks(title="Pro Thumbnail Maker (Rembg)") as app:
    selected_idx = gr.State(value=0)
    
    gr.Markdown("# 🎬 Pro YouTube Thumbnail Maker (Rembg Edition)")
    gr.Markdown("Pilih frame yang ingin dijadikan subjek utama, AI akan menghapus background-nya secara otomatis.")

    with gr.Row():
        with gr.Column():
            v_input = gr.Video(label="1. Upload Video")
            status = gr.Textbox(label="Status", interactive=False)
            headline = gr.Textbox(label="2. Masukkan Headline", placeholder="Contoh: DATA JADI KUASA")
            btn_gen = gr.Button("🚀 Generate Thumbnail", variant="primary", size="lg")
            
        with gr.Column():
            gallery = gr.Gallery(label="3. Pilih Frame Subjek", columns=4, object_fit="contain", height=400)
            output_img = gr.Image(label="Hasil Final")

    # Event Handlers
    v_input.change(process_video, v_input, [gallery, status])
    
    # Simpan index galeri saat diklik
    def update_selection(evt: gr.SelectData):
        if evt is not None:
            return evt.index
        return 0

    gallery.select(update_selection, None, selected_idx)
    
    # Klik tombol generate
    # --- EVENT HANDLERS ---
    # Pastikan fungsi pendukung didefinisikan dengan benar
    def on_select(evt: gr.SelectData):
        return evt.index

    # Event saat video diupload/diganti
    v_input.change(
        fn=process_video, 
        inputs=[v_input], 
        outputs=[gallery, status]
    )

    # Event saat gambar di galeri diklik
    gallery.select(
        fn=on_select, 
        outputs=[selected_idx]
    )

    # Event saat tombol generate diklik
    btn_gen.click(
        fn=generate, 
        inputs=[selected_idx, headline], 
        outputs=[output_img]
    )

if __name__ == "__main__":
    app.launch()