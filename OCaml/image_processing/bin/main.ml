open Image_processing

let () =
  let img = PPM_images.open_ppm "src/adrien.pnm" in
  let rgb_img = PPM_images.ppm_to_rgb img in
  Display.display_rgb_image rgb_img ~scale:0.5 ~scaling_algorithm:Resize.Bicubic
    ~open_window:true 0 0
