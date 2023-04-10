(* type t1 = [ `String of string | `EOF ]
      type t2 = [ `String of string | `EOL ]

   let print_string = function
      | `String t -> print_endline t
      | _ -> print_newline ()

   let () =
      let a : t1 = `String "hello" and b : t2 = `String "world" and c : t2 = `EOL in
      print_string a;
      print_string b;
      print_string c *)

(* type number_generator = [ `Int of int ] -> int

   let global_generator : number_generator =
     let start = ref 0 in
     function
     | `Int n ->
         start := !start + n;
         !start

   let next_int (gen : number_generator) = gen (`Int 1)

   let () =
     let gen : number_generator = global_generator in
     for _ = 0 to 10 do
       Printf.printf "%d\n" (next_int gen)
     done *)

type number_generator = int -> int

let generator ~(start : int) : number_generator =
  let offset = ref 0 in
  function
  | n ->
      offset := !offset + n;
      !offset + start

let next (gen : number_generator) = gen 1

let next_even (gen : number_generator) =
  match gen 1 with n when n mod 2 = 0 -> n | _ -> gen 1

let next_odd (gen : number_generator) =
  match gen 1 with n when n mod 2 = 1 -> n | _ -> gen 1

let rec next_square (gen : number_generator) =
  match gen 1 with
  | n when float_of_int n |> sqrt |> Float.round = (float_of_int n |> sqrt) -> n
  | _ -> next_square gen

let rec next_prime (gen : number_generator) =
  let is_prime n =
    let rec no_divisors m =
      m * m > n || (n mod m != 0 && no_divisors (m + 1))
    in
    n >= 2 && no_divisors 2
  in
  match gen 1 with n when is_prime n -> n | _ -> next_prime gen

let () =
  let gen : number_generator = generator ~start:10 in
  for _ = 0 to 10 do
    Printf.printf "%d\n" (next_prime gen)
  done
