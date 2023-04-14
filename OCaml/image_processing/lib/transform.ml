open Images

let crop_img src x y width height =
  let pixels = Array.make_matrix height width 0 in
  for i = 0 to height - 1 do
    for j = 0 to width - 1 do
      pixels.(i).(j) <- src.pixels.(i + y).(j + x)
    done
  done;
  { width; height; pixels }

let rotate_90_left src =
  let n, m = (Array.length src.pixels, Array.length src.pixels.(0)) in
  let rotated_mat = Array.make_matrix m n 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      rotated_mat.(m - 1 - j).(i) <- src.pixels.(i).(j)
    done
  done;
  { width = n; height = m; pixels = rotated_mat }

let rotate_90_right src =
  let n, m = (Array.length src.pixels, Array.length src.pixels.(0)) in
  let rotated_mat = Array.make_matrix m n 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      rotated_mat.(j).(n - 1 - i) <- src.pixels.(i).(j)
    done
  done;
  { width = n; height = m; pixels = rotated_mat }

let rotate_180 src =
  let n, m = (Array.length src.pixels, Array.length src.pixels.(0)) in
  let rotated_mat = Array.make_matrix n m 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      rotated_mat.(n - 1 - i).(m - 1 - j) <- src.pixels.(i).(j)
    done
  done;
  { width = m; height = n; pixels = rotated_mat }

(* clockwise rotation by [degrees]° *)
let rotate_angle src (degrees : float) =
  let shear angle x y =
    let tangent = Float.tan (angle /. 2.) in
    (* shear 1 *)
    let new_x = x -. (y *. tangent) |> Float.round and new_y = y in
    (* shear 2 *)
    let new_y = (new_x *. Float.sin angle) +. new_y |> Float.round in
    (* shear 3 *)
    let new_x = new_x -. (new_y *. tangent) |> Float.round in
    (int new_x, int new_y)
  in
  let angle = degrees *. (Float.pi /. 180.) in
  let cosine = Float.cos angle
  and sine = Float.sin angle
  and height = src.height
  and width = src.width in
  let new_height =
    Float.abs (float height *. cosine) +. Float.abs (float width *. sine) +. 1.
    |> Float.round |> int
  and new_width =
    Float.abs (float width *. cosine) +. Float.abs (float height *. sine) +. 1.
    |> Float.round |> int
  in
  let output = Array.make_matrix new_height new_width 0 in
  let original_center_height =
    ((float height +. 1.) /. 2.) -. 1. |> Float.round |> int
  and original_center_width =
    ((float width +. 1.) /. 2.) -. 1. |> Float.round |> int
  in
  let new_center_height =
    ((float new_height +. 1.) /. 2.) -. 1. |> Float.round |> int
  and new_center_width =
    ((float new_width +. 1.) /. 2.) -. 1. |> Float.round |> int
  in
  for i = 0 to height - 1 do
    for j = 0 to width - 1 do
      let y = height - 1 - i - original_center_height |> float
      and x = width - 1 - j - original_center_width |> float in
      let new_x, new_y = shear angle x y in
      let new_y = new_center_height - new_y
      and new_x = new_center_width - new_x in
      if 0 <= new_x && new_x < new_width && 0 <= new_y && new_y < new_height
      then output.(new_y).(new_x) <- src.pixels.(i).(j)
    done
  done;
  { width = new_width; height = new_height; pixels = output }

let flip_horizontal src =
  let n, m = (Array.length src.pixels, Array.length src.pixels.(0)) in
  let rotated_mat = Array.make_matrix n m 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      rotated_mat.(i).(m - 1 - j) <- src.pixels.(i).(j)
    done
  done;
  { width = m; height = n; pixels = rotated_mat }

let flip_vertical src =
  let n, m = (Array.length src.pixels, Array.length src.pixels.(0)) in
  let rotated_mat = Array.make_matrix n m 0 in
  for i = 0 to n - 1 do
    for j = 0 to m - 1 do
      rotated_mat.(n - 1 - i).(j) <- src.pixels.(i).(j)
    done
  done;
  { width = m; height = n; pixels = rotated_mat }

let generate_gaussian_filter (sigma : float) (m : int) (n : int) =
  let m_half = m / 2
  and n_half = n / 2
  and gaussian_filter = Array.init m (fun _ -> Array.make n 0.) in
  for y = -m_half to m_half - 1 do
    for x = -n_half to n_half - 1 do
      let normal = 1. /. (2. *. Float.pi *. (sigma ** 2.))
      and exp_term =
        Float.exp
          (-.((float x ** 2.) +. (float y ** 2.)) /. (2. *. (sigma ** 2.)))
      in
      gaussian_filter.(y + m_half).(x + n_half) <- normal *. exp_term
    done
  done;
  gaussian_filter

(* let convolution ?(stride : int * int = (1, 1)) ?(dilation : int * int = (1, 1))
     ?(padding : int * int = (0, 0)) (img : rgb_image)
     (kernel : float array array) =
   let add_padding img padding =
     let n, m = (Array.length img.pixels, Array.length img.pixels.(0))
     and r, c = padding in
     let padded_matrix = Array.make_matrix (n + (r * 2)) (m + (c * 2)) 0 in
     for i = 0 to n - 1 do
       for j = 0 to m - 1 do
         padded_matrix.(i + r).(j + c) <- img.pixels.(i).(j)
       done
     done;
     { width = m + (c * 2); height = n + (r * 2); pixels = padded_matrix }
   in

   let out_size n m n_k m_k stride dilation padding =
     let n_s, m_s = stride and n_d, m_d = dilation and n_p, m_p = padding in
     ( (float n
       +. (2. *. float n_p)
       -. float n_k
       -. ((float n_k -. 1.) *. (float n_d -. 1.)))
       /. float n_s
       |> Float.floor |> int |> ( + ) 1,
       (float m
       +. (2. *. float m_p)
       -. float m_k
       -. ((float m_k -. 1.) *. (float m_d -. 1.)))
       /. float m_s
       |> Float.floor |> int |> ( + ) 1 )
   in

   let img = add_padding img padding in
   let n_p, m_p = (Array.length img.pixels, Array.length img.pixels.(0))
   and n_k, m_k = (Array.length kernel, Array.length kernel.(0)) in
   let h_out, w_out = out_size n_p m_p n_k m_k stride dilation padding in
   let matrix_out = Array.make_matrix h_out w_out 0 in
   let n_b, m_b = (n_k / 2, m_k / 2) in
   let n_d, m_d = dilation in
   let n_s, m_s = stride in
   let center_x_0, center_y_0 = (n_b * n_d, m_b * m_d) in
   for i = 0 to h_out - 1 do
     let center_x = center_x_0 + (i * n_s) in
     let indices_x =
       Array.init (2 * n_b) (fun l -> center_x * (l - n_b) * n_d)
     in
     for j = 0 to w_out - 1 do
       let center_y = center_y_0 + (j * m_s) in
       let indices_y =
         Array.init (2 * m_b) (fun l -> center_y * (l - m_b) * m_d)
       in
       let sub_matrix = filter_matrix img.pixels indices_x indices_y in
       let red_matrix =
         Array.map
           (fun row ->
             Array.map
               (fun value ->
                 let r, _, _ = of_rgb value in
                 float r)
               row)
           sub_matrix
       and green_matrix =
         Array.map
           (fun row ->
             Array.map
               (fun value ->
                 let _, g, _ = of_rgb value in
                 float g)
               row)
           sub_matrix
       and blue_matrix =
         Array.map
           (fun row ->
             Array.map
               (fun value ->
                 let _, _, b = of_rgb value in
                 float b)
               row)
           sub_matrix
       in
       matrix_out.(i).(j) <-
         to_rgb
           (Array.fold_left
              (fun acc row -> Array.fold_left ( +. ) 0. row)
              0. (red_matrix *>. kernel)
           |> int)
           (Array.fold_left
              (fun acc row -> Array.fold_left ( +. ) 0. row)
              0. (green_matrix *>. kernel)
           |> int)
           (Array.fold_left
              (fun acc row -> Array.fold_left ( +. ) 0. row)
              0. (blue_matrix *>. kernel)
           |> int)
     done
   done;
   { width = img.width; height = img.height; pixels = matrix_out } *)

let convolve src kernel =
  let add_padding img padding =
    let n, m = (Array.length img.pixels, Array.length img.pixels.(0))
    and r, c = padding in
    let padded_matrix = Array.make_matrix (n + (r * 2)) (m + (c * 2)) 0 in
    for i = 0 to n - 1 do
      for j = 0 to m - 1 do
        padded_matrix.(i + r).(j + c) <- img.pixels.(i).(j)
      done
    done;
    { width = m + (c * 2); height = n + (r * 2); pixels = padded_matrix }
  in
  let width, height = (src.width, src.height)
  and size_x, size_y = (Array.length kernel.(0), Array.length kernel) in
  let m_p, n_p = (size_x / 2, size_y / 2) in
  let output =
    Array.make_matrix
      (height - size_y + (2 * n_p) + 1)
      (width - size_x + (2 * m_p) + 1)
      0
  in
  let padded_image = add_padding src (n_p, m_p) in
  for x = 0 to padded_image.width - size_x do
    for y = 0 to padded_image.height - size_y do
      let window = crop_img padded_image x y size_x size_y in
      let red_matrix =
        Array.map
          (fun row ->
            Array.map
              (fun value ->
                let r, _, _ = of_rgb value in
                float r)
              row)
          window.pixels
      and green_matrix =
        Array.map
          (fun row ->
            Array.map
              (fun value ->
                let _, g, _ = of_rgb value in
                float g)
              row)
          window.pixels
      and blue_matrix =
        Array.map
          (fun row ->
            Array.map
              (fun value ->
                let _, _, b = of_rgb value in
                float b)
              row)
          window.pixels
      in
      output.(y).(x) <-
        to_rgb
          (Array.map2 (Array.map2 ( *. )) kernel red_matrix
          |> Array.map (Array.fold_left ( +. ) 0.)
          |> Array.fold_left ( +. ) 0. |> int)
          (Array.map2 (Array.map2 ( *. )) kernel green_matrix
          |> Array.map (Array.fold_left ( +. ) 0.)
          |> Array.fold_left ( +. ) 0. |> int)
          (Array.map2 (Array.map2 ( *. )) kernel blue_matrix
          |> Array.map (Array.fold_left ( +. ) 0.)
          |> Array.fold_left ( +. ) 0. |> int)
    done
  done;
  { width; height; pixels = output }

let normalize kernel =
  let sum =
    Array.map (Array.fold_left ( +. ) 0.) kernel |> Array.fold_left ( +. ) 0.
  in
  if sum = 0. then kernel else Array.map (Array.map (fun x -> x /. sum)) kernel

let gaussian_blur img sigma =
  let kernel = generate_gaussian_filter sigma 5 5 |> normalize in
  convolve img kernel

let edge img =
  let kernel =
    [| [| -1.; -1.; -1. |]; [| -1.; 8.; -1. |]; [| -1.; -1.; -1. |] |]
  in
  convolve img kernel

let box_blur img =
  let kernel =
    [| [| 1.; 1.; 1. |]; [| 1.; 1.; 1. |]; [| 1.; 1.; 1. |] |] |> normalize
  in
  convolve img kernel

let sharpen img =
  let kernel = [| [| 0.; -1.; 0. |]; [| -1.; 5.; -1. |]; [| 0.; -1.; 0. |] |] in
  convolve img kernel
