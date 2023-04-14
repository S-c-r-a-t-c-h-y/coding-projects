exception Corrupted_image of string

type rgb_image = { width : int; height : int; pixels : int array array }
type chunk_reader_error = [ `End_of_file of int ]

type chunk_reader =
  [ `Bytes of int | `Close ] -> (string, chunk_reader_error) result

let chunk_reader_of_in_channel ich : chunk_reader = function
  | `Bytes num_bytes -> (
      try Ok (really_input_string ich num_bytes) with
      | End_of_file ->
          let offset = pos_in ich in
          close_in ich;
          Error (`End_of_file offset)
      | e ->
          close_in ich;
          raise e)
  | `Close ->
      close_in ich;
      Ok ""

let chunk_reader_of_path fn = chunk_reader_of_in_channel (open_in_bin fn)

let get_bytes (reader : chunk_reader) num_bytes =
  reader (`Bytes num_bytes) |> function
  | Ok x -> x
  | Error (`End_of_file _) -> raise End_of_file

let chunk_char (reader : chunk_reader) = String.get (get_bytes reader 1) 0
let chunk_byte (reader : chunk_reader) = chunk_char reader |> Char.code
let close_chunk_reader (reader : chunk_reader) = ignore (reader `Close)
let int = int_of_float
let to_rgb r g b = (r lsl 16) lor (g lsl 8) lor b

let of_rgb rgb_value =
  ((rgb_value lsr 16) land 255, (rgb_value lsr 8) land 255, rgb_value land 255)

let avg_rgb rgb1 rgb2 = (rgb1 + rgb2) lsr 1

let split_colors color_matrix =
  let red_matrix =
    Array.map
      (fun row ->
        Array.map
          (fun value ->
            let r, _, _ = of_rgb value in
            r)
          row)
      color_matrix
  and green_matrix =
    Array.map
      (fun row ->
        Array.map
          (fun value ->
            let _, g, _ = of_rgb value in
            g)
          row)
      color_matrix
  and blue_matrix =
    Array.map
      (fun row ->
        Array.map
          (fun value ->
            let _, _, b = of_rgb value in
            b)
          row)
      color_matrix
  in
  (red_matrix, green_matrix, blue_matrix)

let copy_img img =
  { width = img.width; height = img.height; pixels = Array.copy img.pixels }

let inverse_rgb_img img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col lxor 0xffffff) row)
        img.pixels;
  }

let filter_red img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col land 0xff0000) row)
        img.pixels;
  }

let filter_green img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col land 0x00ff00) row)
        img.pixels;
  }

let filter_blue img =
  {
    width = img.width;
    height = img.height;
    pixels =
      Array.map
        (fun row -> Array.map (fun col -> col land 0x0000ff) row)
        img.pixels;
  }

let filter_matrix mat inds_x inds_y =
  let filter_array arr inds =
    arr |> Array.to_list
    |> List.filteri (fun i _ -> Array.mem i inds)
    |> Array.of_list
  in
  filter_array mat inds_y |> Array.map (fun x -> filter_array x inds_x)

(* float matrix mutliplication *)
let ( *>. ) x y =
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

(* integers matrix multiplication *)
let ( *> ) x y =
  let x0 = Array.length x and y0 = Array.length y in
  let y1 = if y0 = 0 then 0 else Array.length y.(0) in
  let z = Array.make_matrix x0 y1 0 in
  for i = 0 to x0 - 1 do
    for j = 0 to y1 - 1 do
      for k = 0 to y0 - 1 do
        z.(i).(j) <- z.(i).(j) + (x.(i).(k) * y.(k).(j))
      done
    done
  done;
  z
