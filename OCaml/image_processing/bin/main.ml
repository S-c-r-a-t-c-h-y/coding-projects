open Image_processing

let () =
  let img = PPM_images.open_ppm "src/adrien.pnm" in
  let rgb_img = PPM_images.ppm_to_rgb img in
  let inv_img = Filter.inverse rgb_img in
  let red_img = Filter.red rgb_img in
  let green_img = Filter.green rgb_img in
  let blue_img = Filter.blue rgb_img in
  (* let cropped_img = Transform.crop_img rgb_img 200 200 512 512 in *)
  let rotated_img = Transform.rotate_angle rgb_img 90. in
  let flipped_img = Transform.flip_horizontal rgb_img in
  let blured_img = Transform.gaussian_blur rgb_img 5. 9 in
  let blured_img2 = Transform.box_blur rgb_img in
  let sharpened_img = Transform.sharpen rgb_img in
  let edged_img = Transform.edge rgb_img in
  let vignette_img = Filter.vignette rgb_img 200. in
  let bright_img = Filter.brighten rgb_img 100 in
  Printf.ksprintf Graphics.open_graph " %dx%d" (rgb_img.width * 2)
    rgb_img.height;
  Display.display_rgb_image rgb_img ~scale:1. ~scaling_algorithm:Resize.Auto 0 0;
  Display.display_rgb_image sharpened_img ~scale:1.
    ~scaling_algorithm:Resize.Auto rgb_img.width 0;
  Display.hande_graph_closing ()
