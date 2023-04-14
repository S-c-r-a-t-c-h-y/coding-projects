open Image_processing

let () =
  let img = PPM_images.open_ppm "src/adrien.pnm" in
  let rgb_img = PPM_images.ppm_to_rgb img in
  (* let inv_img = Images.inverse_rgb_img rgb_img in
     let red_img = Images.filter_red rgb_img in
     let green_img = Images.filter_green rgb_img in
     let blue_img = Images.filter_blue rgb_img in
     let cropped_img = Transform.crop_img rgb_img 200 200 512 512 in
     let rotated_img = Transform.rotate_angle rgb_img 90. in
     let flipped_img = Transform.flip_horizontal rgb_img in *)
  (* let blured_img = Transform.gaussian_blur rgb_img 5. in
     let blured_img2 = Transform.box_blur rgb_img in *)
  let sharpened_img = Transform.sharpen rgb_img in
  let edged_img = Transform.edge rgb_img in
  Display.display_rgb_image sharpened_img ~scale:0.5
    ~scaling_algorithm:Resize.Auto ~open_window:true 0 0
