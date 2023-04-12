open Images

type ppm_pixels =
  | P1 of int array array
  | P2 of int array array
  | P3 of (int * int * int) array array
  | P4 of int array array
  | P5 of int array array
  | P6 of (int * int * int) array array

type ppm_image = {
  width : int;
  height : int;
  max_value : int;
  pixels : ppm_pixels;
}

(* let inverse ppm = {width=ppm.width; height=ppm.height; max_value=ppm.max_value; pixels = } *)

let ppm_to_rgb (ppm : ppm_image) =
  match ppm.pixels with
  | P1 pixels | P2 pixels | P4 pixels | P5 pixels ->
      {
        width = ppm.width;
        height = ppm.height;
        pixels =
          Array.map
            (Array.map (fun x ->
                 let v = x * 255 / ppm.max_value in
                 to_rgb v v v))
            pixels;
      }
  | P3 pixels | P6 pixels ->
      {
        width = ppm.width;
        height = ppm.height;
        pixels =
          Array.map
            (Array.map (fun (r, g, b) ->
                 to_rgb
                   (r * 255 / ppm.max_value)
                   (g * 255 / ppm.max_value)
                   (b * 255 / ppm.max_value)))
            pixels;
      }

let read_header (content : chunk_reader) =
  let magic = ref "" in
  let width = ref (-1) and height = ref (-1) in
  let max_val = ref 1 in
  let scanner = Scanf.Scanning.from_function (fun () -> chunk_char content) in
  let rec pass_comments () =
    try
      Scanf.bscanf scanner "#%[^\n\r]%[\t\n\r]" (fun _ _ -> ());
      pass_comments ()
    with _ -> ()
  in
  Scanf.bscanf scanner "%s%[\t\n ]" (fun mn _ -> magic := mn);
  pass_comments ();

  if not (List.mem !magic [ "P1"; "P2"; "P3"; "P4"; "P5"; "P6" ]) then
    raise (Corrupted_image "PPM : invalid magic number");

  if List.mem !magic [ "P1"; "P4" ] then (
    Scanf.bscanf scanner "%u%[\t\n ]" (fun w _ -> width := w);
    pass_comments ();
    Scanf.bscanf scanner "%u%1[\t\n ]" (fun h _ -> height := h))
  else (
    (try Scanf.bscanf scanner "%u%[\t\n ]" (fun w _ -> width := w)
     with Stdlib.Scanf.Scan_failure _ ->
       raise (Corrupted_image "PPM: invalid width"));
    pass_comments ();
    (try Scanf.bscanf scanner "%u%[\t\n ]" (fun h _ -> height := h)
     with Stdlib.Scanf.Scan_failure _ ->
       raise (Corrupted_image "PPM: invalid height"));
    pass_comments ();
    try Scanf.bscanf scanner "%u%1[\t\n ]" (fun mv _ -> max_val := mv)
    with Stdlib.Scanf.Scan_failure _ ->
      raise (Corrupted_image "PPM: invalid max_val"));
  (!magic, !width, !height, !max_val, scanner)

let parse_ppm (ich : chunk_reader) : ppm_image =
  let prev_byte = ref None in
  try
    let magic, width, height, max_val, scanner =
      (function
        | `Bytes 1 ->
            let b = ich (`Bytes 1) in
            prev_byte := Some b;
            b
        | orig -> ich orig)
      |> read_header
    in
    let content : chunk_reader = function
      | `Bytes 1 -> (
          match !prev_byte with
          | Some x ->
              prev_byte := None;
              x
          | None -> ich (`Bytes 1))
      | orig -> ich orig
    in

    (* CONTENT PARSING *)
    match magic with
    | "P1" | "P2" ->
        let pixels =
          Array.init height (fun _ -> Array.init width (fun _ -> 0))
        in
        for y = 0 to height - 1 do
          for x = 0 to width - 1 do
            try
              Scanf.bscanf scanner "%d%[\t\n ]" (fun v _ -> pixels.(y).(x) <- v)
            with Stdlib.Scanf.Scan_failure _ ->
              raise (Corrupted_image "PPM: Invalid grayscale pixel data")
          done
        done;
        if magic = "P1" then
          { width; height; max_value = max_val; pixels = P1 pixels }
        else { width; height; max_value = max_val; pixels = P2 pixels }
    | "P3" ->
        let pixels =
          Array.init height (fun _ -> Array.init width (fun _ -> (0, 0, 0)))
        in
        for y = 0 to height - 1 do
          for x = 0 to width - 1 do
            Scanf.bscanf scanner "%d%[\t\n ]%d%[\t\n ]%d%[\t\n ]"
              (fun r _ g _ b _ -> pixels.(y).(x) <- (r, g, b))
          done
        done;
        { width; height; max_value = max_val; pixels = P3 pixels }
    | "P4" ->
        let pixels =
          Array.init height (fun _ -> Array.init width (fun _ -> 0))
        in
        for y = 0 to height - 1 do
          let x = ref 0 in
          let byte = ref 0 in
          while !x < width do
            if !x mod 8 = 0 then byte := chunk_byte content;
            let byte_pos = !x mod 8 in
            let v = (!byte lsr (7 - byte_pos)) land 1 in
            pixels.(y).(!x) <- v;
            incr x
          done
        done;
        { width; height; max_value = 1; pixels = P4 pixels }
    | "P5" ->
        let pixels =
          Array.init height (fun _ -> Array.init width (fun _ -> 0))
        in
        for y = 0 to height - 1 do
          for x = 0 to width - 1 do
            if max_val <= 255 then
              let b0 = chunk_byte content in
              pixels.(y).(x) <- b0
            else
              let b0 = chunk_byte content in
              let b1 = chunk_byte content in
              pixels.(y).(x) <- (b0 lsl 8) + b1
          done
        done;
        { width; height; max_value = max_val; pixels = P5 pixels }
    | "P6" ->
        let pixels =
          Array.init height (fun _ -> Array.init width (fun _ -> (0, 0, 0)))
        in
        for y = 0 to height - 1 do
          for x = 0 to width - 1 do
            if max_val <= 255 then
              let r = chunk_byte content in
              let g = chunk_byte content in
              let b = chunk_byte content in
              pixels.(y).(x) <- (r, g, b)
            else
              let r1 = chunk_byte content in
              let r0 = chunk_byte content in
              let g1 = chunk_byte content in
              let g0 = chunk_byte content in
              let b1 = chunk_byte content in
              let b0 = chunk_byte content in
              let r = (r1 lsl 8) + r0 in
              let g = (g1 lsl 8) + g0 in
              let b = (b1 lsl 8) + b0 in
              pixels.(y).(x) <- (r, g, b)
          done
        done;
        { width; height; max_value = max_val; pixels = P6 pixels }
    | _ -> raise (Corrupted_image "Invalid PPM format")
  with End_of_file -> raise (Corrupted_image "Truncated file")

let open_ppm img =
  let ich = chunk_reader_of_path img in
  parse_ppm ich
