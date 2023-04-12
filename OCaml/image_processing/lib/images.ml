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

let to_gray_scale arr =
  Array.map (fun x -> Array.map (fun (r, g, b) -> (r + b + g) / 3) x) arr

let to_rgb r g b = (r lsl 16) lor (g lsl 8) lor b

let of_rgb rgb_value =
  ((rgb_value lsr 16) land 255, (rgb_value lsr 8) land 255, rgb_value land 255)

let avg_rgb rgb1 rgb2 =
  let r1, g1, b1 = of_rgb rgb1 and r2, g2, b2 = of_rgb rgb2 in
  to_rgb ((r1 + r2) / 2) ((g1 + g2) / 2) ((b1 + b2) / 2)
