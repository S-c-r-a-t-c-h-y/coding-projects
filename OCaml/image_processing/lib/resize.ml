open Images

type algorithm = Nearest | Bilinear | Box | Bicubic

(* Nearest neighbor interpolation *)
let resize_nearest ~(src : rgb_image) (new_width : int) (new_height : int) =
  let scale_x = float_of_int new_width /. float_of_int src.width
  and scale_y = float_of_int new_height /. float_of_int src.height
  and new_img =
    {
      width = new_width;
      height = new_height;
      pixels = Array.init new_height (fun _ -> Array.make new_width 0);
    }
  in
  for y = 0 to new_height - 1 do
    for x = 0 to new_width - 1 do
      let x_nearest = float_of_int x /. scale_x |> Float.floor |> int_of_float
      and y_nearest =
        float_of_int y /. scale_y |> Float.floor |> int_of_float
      in
      let pixel = src.pixels.(y_nearest).(x_nearest) in
      new_img.pixels.(y).(x) <- pixel
    done
  done;
  new_img

(* bilinear interpolation *)
let resize_bilinear ~(src : rgb_image) (new_width : int) (new_height : int) =
  let bilinear_interpolation q11 q12 q21 q22 x1 x2 y1 y2 old_x old_y =
    let r11, g11, b11 = of_rgb q11
    and r12, g12, b12 = of_rgb q12
    and r21, g21, b21 = of_rgb q21
    and r22, g22, b22 = of_rgb q22 in
    if x1 <> x2 then
      let rp1, gp1, bp1 =
        ( ((float_of_int x2 -. old_x) *. float_of_int r11)
          +. ((old_x -. float_of_int x1) *. float_of_int r12),
          ((float_of_int x2 -. old_x) *. float_of_int g11)
          +. ((old_x -. float_of_int x1) *. float_of_int g12),
          ((float_of_int x2 -. old_x) *. float_of_int b11)
          +. ((old_x -. float_of_int x1) *. float_of_int b12) )
      and rp2, gp2, bp2 =
        ( ((float_of_int x2 -. old_x) *. float_of_int r21)
          +. ((old_x -. float_of_int x1) *. float_of_int r22),
          ((float_of_int x2 -. old_x) *. float_of_int g21)
          +. ((old_x -. float_of_int x1) *. float_of_int g22),
          ((float_of_int x2 -. old_x) *. float_of_int b21)
          +. ((old_x -. float_of_int x1) *. float_of_int b22) )
      in
      if y1 <> y2 then
        let rp, gp, bp =
          ( ((float_of_int y2 -. old_y) *. rp1)
            +. ((old_y -. float_of_int y1) *. rp2),
            ((float_of_int y2 -. old_y) *. gp1)
            +. ((old_y -. float_of_int y1) *. gp2),
            ((float_of_int y2 -. old_y) *. bp1)
            +. ((old_y -. float_of_int y1) *. bp2) )
        in
        to_rgb
          (rp |> Float.round |> int_of_float)
          (gp |> Float.round |> int_of_float)
          (bp |> Float.round |> int_of_float)
      else
        to_rgb
          (rp1 |> Float.round |> int_of_float)
          (gp1 |> Float.round |> int_of_float)
          (bp1 |> Float.round |> int_of_float)
    else if y1 <> y2 then
      let rp, gp, bp =
        ( ((float_of_int y2 -. old_y) *. float_of_int r11)
          +. ((old_y -. float_of_int y1) *. float_of_int r22),
          ((float_of_int y2 -. old_y) *. float_of_int g11)
          +. ((old_y -. float_of_int y1) *. float_of_int g22),
          ((float_of_int y2 -. old_y) *. float_of_int b11)
          +. ((old_y -. float_of_int y1) *. float_of_int b22) )
      in
      to_rgb
        (rp |> Float.round |> int_of_float)
        (gp |> Float.round |> int_of_float)
        (bp |> Float.round |> int_of_float)
    else q11
  in
  let scale_x = float_of_int new_width /. float_of_int src.width
  and scale_y = float_of_int new_height /. float_of_int src.height
  and new_img =
    {
      width = new_width;
      height = new_height;
      pixels = Array.init new_height (fun _ -> Array.make new_width 0);
    }
  in
  for y = 0 to new_height - 1 do
    for x = 0 to new_width - 1 do
      (* coordinates in old image *)
      let old_x = float_of_int x /. scale_x
      and old_y = float_of_int y /. scale_y in

      (* finding nearest points *)
      let x1 = old_x |> Float.floor |> int_of_float |> min (src.width - 1)
      and y1 = old_y |> Float.floor |> int_of_float |> min (src.height - 1)
      and x2 = old_x |> Float.ceil |> int_of_float |> min (src.width - 1)
      and y2 = old_y |> Float.ceil |> int_of_float |> min (src.height - 1) in

      let q11 = src.pixels.(y1).(x1)
      and q12 = src.pixels.(y1).(x2)
      and q21 = src.pixels.(y2).(x1)
      and q22 = src.pixels.(y2).(x2) in

      let pixel =
        bilinear_interpolation q11 q12 q21 q22 x1 x2 y1 y2 old_x old_y
      in
      new_img.pixels.(y).(x) <- pixel
    done
  done;
  new_img

(* box sampling *)
let resize_box ~(src : rgb_image) (new_width : int) (new_height : int) =
  let avg_box (pixels : int array array) x1 x2 y1 y2 =
    let avg_line (line : int array) =
      let avg = line.(x1) |> ref in
      for i = 0 to Array.length line - 1 do
        if x1 <= i && i <= x2 then avg := avg_rgb !avg line.(i)
      done;
      !avg
    in
    let avg = avg_line pixels.(y1) |> ref in
    for i = 0 to Array.length pixels - 1 do
      if y1 <= i && i <= y2 then avg := avg_rgb !avg (avg_line pixels.(i))
    done;
    !avg
  in
  let scale_x = float_of_int new_width /. float_of_int src.width
  and scale_y = float_of_int new_height /. float_of_int src.height
  and new_img =
    {
      width = new_width;
      height = new_height;
      pixels = Array.init new_height (fun _ -> Array.make new_width 0);
    }
  in
  let box_width = 1. /. scale_x |> Float.ceil |> int_of_float
  and box_height = 1. /. scale_y |> Float.ceil |> int_of_float in
  for y = 0 to new_height - 1 do
    for x = 0 to new_width - 1 do
      let old_x = float_of_int x /. scale_x |> Float.floor |> int_of_float
      and old_y = float_of_int y /. scale_y |> Float.floor |> int_of_float in
      let x_end = min (old_x + box_width) (src.width - 1)
      and y_end = min (old_y + box_height) (src.height - 1) in
      let pixel = avg_box src.pixels old_x x_end old_y y_end in
      new_img.pixels.(y).(x) <- pixel
    done
  done;
  new_img

let resize_bicubic ~(src : rgb_image) ?(a : float = -0.5) (scale : float) =
  let matrix_multiply x y =
    let x0 = Array.length x and y0 = Array.length y in
    let y1 = if y0 = 0 then 0 else Array.length y.(0) in
    let z = Array.make_matrix x0 y1 0. in
    for i = 0 to x0 - 1 do
      for j = 0 to y1 - 1 do
        for k = 0 to y0 - 1 do
          z.(i).(j) <- z.(i).(j) +. (x.(i).(k) *. y.(k).(j))
        done
      done
    done;
    z
  in

  let u s a =
    if abs_float s >= 0. && abs_float s <= 1. then
      ((a +. 2.) *. (abs_float s ** 3.))
      -. ((a +. 3.) *. (abs_float s ** 2.))
      +. 1.
    else if abs_float s > 1. && abs_float s <= 2. then
      (a *. (abs_float s ** 3.))
      -. (5. *. a *. (abs_float s ** 2.))
      +. (8. *. a *. abs_float s)
      -. (4. *. a)
    else 0.
  in

  let padding img w h =
    let zimg = Array.init (h + 4) (fun _ -> Array.make (w + 4) 0) in
    for i = 0 to h - 1 do
      for j = 0 to w - 1 do
        zimg.(i + 2).(j + 2) <- img.(i).(j)
      done;
      for j = 0 to 1 do
        zimg.(i + 2).(j) <- img.(i).(j);
        zimg.(i + 2).(j + 2 + w) <- img.(i).(w - 2 + j);

        zimg.(j).(j) <- img.(0).(0);
        zimg.(h + j + 2).(j) <- img.(h - 1).(0);
        zimg.(h + j + 2).(w + j + 2) <- img.(h - 1).(w - 1);
        zimg.(j).(w + j + 2) <- img.(0).(w - 1)
      done
    done;
    for i = 0 to w - 1 do
      for j = 0 to 1 do
        zimg.(j).(i + 2) <- img.(j).(i);
        zimg.(j + 2 + h).(i + 2) <- img.(h - 2 + j).(i)
      done
    done;
    zimg
  in

  let w = src.width and h = src.height in
  let img = padding src.pixels w h in
  let new_width = float_of_int w *. scale |> Float.floor |> int_of_float
  and new_height = float_of_int h *. scale |> Float.floor |> int_of_float in
  let new_img =
    {
      width = new_width;
      height = new_height;
      pixels = Array.init new_height (fun _ -> Array.make new_width 0);
    }
  and h = 1. /. scale in

  for j = 0 to new_height - 1 do
    for i = 0 to new_width - 1 do
      let x = (float_of_int i *. h) +. 2. and y = (float_of_int j *. h) +. 2. in

      let x1 = 1. +. x -. Float.floor x
      and x2 = x -. Float.floor x
      and x3 = Float.floor x +. 1. -. x
      and x4 = Float.floor x +. 2. -. x
      and y1 = 1. +. y -. Float.floor y
      and y2 = y -. Float.floor y
      and y3 = Float.floor y +. 1. -. y
      and y4 = Float.floor y +. 2. -. y in

      let mat_l = [| [| u x1 a; u x2 a; u x3 a; u x4 a |] |]
      and mat_m =
        [|
          [|
            img.(y -. y1 |> int_of_float).(x -. x1 |> int_of_float);
            img.(y -. y2 |> int_of_float).(x -. x1 |> int_of_float);
            img.(y +. y3 |> int_of_float).(x -. x1 |> int_of_float);
            img.(y +. y4 |> int_of_float).(x -. x1 |> int_of_float);
          |];
          [|
            img.(y -. y1 |> int_of_float).(x -. x2 |> int_of_float);
            img.(y -. y2 |> int_of_float).(x -. x2 |> int_of_float);
            img.(y +. y3 |> int_of_float).(x -. x2 |> int_of_float);
            img.(y +. y4 |> int_of_float).(x -. x2 |> int_of_float);
          |];
          [|
            img.(y -. y1 |> int_of_float).(x +. x3 |> int_of_float);
            img.(y -. y2 |> int_of_float).(x +. x3 |> int_of_float);
            img.(y +. y3 |> int_of_float).(x +. x3 |> int_of_float);
            img.(y +. y4 |> int_of_float).(x +. x3 |> int_of_float);
          |];
          [|
            img.(y -. y1 |> int_of_float).(x +. x4 |> int_of_float);
            img.(y -. y2 |> int_of_float).(x +. x4 |> int_of_float);
            img.(y +. y3 |> int_of_float).(x +. x4 |> int_of_float);
            img.(y +. y4 |> int_of_float).(x +. x4 |> int_of_float);
          |];
        |]
      and mat_r =
        [| [| u y1 a |]; [| u y2 a |]; [| u y3 a |]; [| u y4 a |] |]
      in
      let mat_mr =
        Array.map
          (fun row ->
            Array.map
              (fun value ->
                let r, _, _ = of_rgb value in
                float_of_int r)
              row)
          mat_m
      and mat_mg =
        Array.map
          (fun row ->
            Array.map
              (fun value ->
                let _, g, _ = of_rgb value in
                float_of_int g)
              row)
          mat_m
      and mat_mb =
        Array.map
          (fun row ->
            Array.map
              (fun value ->
                let _, _, b = of_rgb value in
                float_of_int b)
              row)
          mat_m
      in
      (* mat_l x mat_m x mat_r *)
      new_img.pixels.(j).(i) <-
        to_rgb
          ((matrix_multiply mat_mr mat_r |> matrix_multiply mat_l).(0).(0)
          |> int_of_float)
          ((matrix_multiply mat_mg mat_r |> matrix_multiply mat_l).(0).(0)
          |> int_of_float)
          ((matrix_multiply mat_mb mat_r |> matrix_multiply mat_l).(0).(0)
          |> int_of_float)
    done
  done;
  new_img

let scale_image ?(algorithm : algorithm = Bilinear) ~(src : rgb_image)
    (scale : float) =
  let new_width = float_of_int src.width *. scale |> int_of_float
  and new_height = float_of_int src.height *. scale |> int_of_float in
  match algorithm with
  | Nearest -> resize_nearest ~src new_width new_height
  | Bilinear -> resize_bilinear ~src new_width new_height
  | Box -> resize_box ~src new_width new_height
  | Bicubic -> resize_bicubic ~src scale
