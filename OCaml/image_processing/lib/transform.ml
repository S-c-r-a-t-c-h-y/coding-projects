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

let generate_gaussian_filter ?(sigma : float = -1.) (ksize : int) =
  let compute_sigma sigma ksize =
    if sigma < 0. then (0.3 *. (((float ksize -. 1.) *. 0.5) -. 1.)) +. 0.8
    else sigma
  in
  if ksize mod 2 = 0 then raise (Invalid_argument "kernel size must be odd");
  let sigma = compute_sigma sigma ksize in
  let m, n = (ksize, ksize) in
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

let normalize_kernel kernel =
  let sum =
    Array.map (Array.fold_left ( +. ) 0.) kernel |> Array.fold_left ( +. ) 0.
  in
  if sum = 0. then kernel else Array.map (Array.map (fun x -> x /. sum)) kernel

let gaussian_blur img sigma kernel_size =
  let kernel =
    generate_gaussian_filter ~sigma kernel_size |> normalize_kernel
  in
  convolve img kernel

let edge img =
  let kernel =
    [| [| -1.; -1.; -1. |]; [| -1.; 8.; -1. |]; [| -1.; -1.; -1. |] |]
  in
  convolve img kernel

let box_blur img =
  let kernel =
    [| [| 1.; 1.; 1. |]; [| 1.; 1.; 1. |]; [| 1.; 1.; 1. |] |]
    |> normalize_kernel
  in
  convolve img kernel

let sharpen img =
  let kernel = [| [| 0.; -1.; 0. |]; [| -1.; 5.; -1. |]; [| 0.; -1.; 0. |] |] in
  convolve img kernel
