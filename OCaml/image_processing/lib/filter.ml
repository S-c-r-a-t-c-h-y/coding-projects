open Images

let inverse img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lxor 0xffffff) row)
        img.pixels;
  }

let red img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col land 0xff0000) row)
        img.pixels;
  }

let red1 img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lor 0xff0000) row)
        img.pixels;
  }

let red0 img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lor 0xff0000 lxor 0xff0000) row)
        img.pixels;
  }

let green img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col land 0x00ff00) row)
        img.pixels;
  }

let green1 img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lor 0x00ff00) row)
        img.pixels;
  }

let green0 img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lor 0x00ff00 lxor 0x00ff00) row)
        img.pixels;
  }

let blue img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col land 0x0000ff) row)
        img.pixels;
  }

let blue1 img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lor 0x0000ff) row)
        img.pixels;
  }

let blue0 img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lor 0x0000ff lxor 0x0000ff) row)
        img.pixels;
  }

let balance ?(r : int = 0) ?(g : int = 0) ?(b : int = 0) img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (Array.map (fun x ->
             let r_, g_, b_ = of_rgb x in
             to_rgb
               (clamp_color (r_ + r))
               (clamp_color (g_ + g))
               (clamp_color (b_ + b))))
        img.pixels;
  }

let brighten img amt = balance img ~r:amt ~g:amt ~b:amt

let vignette img factor =
  let transpose mat =
    let w, h = (Array.length mat.(0), Array.length mat) in
    let t = Array.make_matrix w h mat.(0).(0) in
    for i = 0 to h - 1 do
      for j = 0 to w - 1 do
        t.(j).(i) <- mat.(i).(j)
      done
    done;
    t
  in
  let gauss std mean x =
    1. /. std *. Float.exp ((-.(x -. mean) ** 2.) /. (2. *. (std ** 2.)))
  in
  let norm vals =
    let min_value = Array.fold_left min vals.(0) vals
    and max_value = Array.fold_left max vals.(0) vals in
    Array.map (fun v -> (v -. min_value) /. (max_value -. min_value)) vals
  in
  let calculate_std arr =
    let mean = Array.fold_left (fun acc v -> (acc +. v) /. 2.) 0. arr in
    let x = Array.map (fun v -> abs_float (v -. mean) ** 2.) arr in
    Array.fold_left (fun acc v -> (acc +. v) /. 2.) 0. x |> Float.sqrt
  in
  let build_gaus width height factor =
    let x_vals = Array.init width (fun i -> float i)
    and y_vals = Array.init height (fun i -> float i) in
    let x_std = calculate_std x_vals and y_std = calculate_std y_vals in
    let x_m = Array.fold_left (fun acc v -> (acc +. v) /. 2.) 0. x_vals
    and y_m = Array.fold_left (fun acc v -> (acc +. v) /. 2.) 0. y_vals in
    let x_gaussian = Array.map (gauss x_std x_m) x_vals |> norm
    and y_gaussian = Array.map (gauss y_std y_m) y_vals |> norm in
    ( Array.map (fun v -> v ** factor) x_gaussian,
      Array.map (fun v -> v ** factor) y_gaussian )
  in
  let x_gaus, y_gaus = build_gaus img.width img.height factor in
  let layer = Array.map (Array.map float) img.pixels in
  let layer = Array.map (Array.map2 ( *. ) x_gaus) layer in
  let layer = Array.map (Array.map2 ( *. ) y_gaus) (transpose layer) in
  {
    width = img.width;
    height = img.height;
    pixels = transpose layer |> Array.map (Array.map int);
  }
