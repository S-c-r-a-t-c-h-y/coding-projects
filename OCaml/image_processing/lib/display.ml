open Images

let hande_graph_closing () : unit =
  while Graphics.read_key () <> 'q' do
    ()
  done;
  Graphics.close_graph ()

let display_rgb_image (img : rgb_image) ?(scale : float = 1.)
    ?(open_window : bool = false)
    ?(scaling_algorithm : Resize.algorithm = Resize.Auto) (x : int) (y : int) =
  let resized_img =
    Resize.scale_image ~algorithm:scaling_algorithm ~src:img scale
  in
  if open_window then
    Printf.ksprintf Graphics.open_graph " %dx%d" resized_img.width
      resized_img.height;
  Graphics.draw_image (Graphics.make_image resized_img.pixels) x y;
  if open_window then hande_graph_closing ()
