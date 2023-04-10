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

(*
   module LinkedList = struct
     type 'a t = Nil | Node of 'a * 'a t

     let create : unit -> 'a t = fun () -> Nil
     let add : 'a -> 'a t -> 'a t = fun e l -> Node (e, l)

     let head : 'a t -> 'a = function
       | Nil -> raise (Failure "LinkedList.head")
       | Node (v, _) -> v

     let tail : 'a t -> 'a t = function
       | Nil -> raise (Failure "LinkedList.tail")
       | Node (_, t) -> t

     let head_opt : 'a t -> 'a option = function
       | Nil -> None
       | Node (v, _) -> Some v

     let tail_opt : 'a t -> 'a t option = function
       | Nil -> None
       | Node (_, t) -> Some t

     let rec length : 'a t -> int = function
       | Nil -> 0
       | Node (_, t) -> 1 + length t

     let init : int -> (int -> 'a) -> 'a t =
      fun n f ->
       let l = create () |> ref in
       for i = n - 1 downto 0 do
         l := add (f i) !l
       done;
       !l

     let rec append : 'a t -> 'a t -> 'a t =
      fun l1 l2 -> match l1 with Nil -> l2 | Node (v, t) -> Node (v, append t l2)
   end

   let () =
     let l = LinkedList.init 10 (fun i -> i) in
     () *)

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

let pp_int_list outchan l =
  let rec print_list = function
    | [] -> ()
    | [ e ] -> Printf.fprintf outchan "%d" e
    | e :: q ->
        Printf.fprintf outchan "%d; " e;
        print_list q
  in
  Printf.fprintf outchan "[";
  print_list l;
  Printf.fprintf outchan "]"

let pp_int_array outchan arr =
  let n = Array.length arr in
  Printf.fprintf outchan "[|";
  for i = 0 to n - 2 do
    Printf.fprintf outchan "%d; " arr.(i)
  done;
  if n <> 0 then Printf.fprintf outchan "%d" arr.(n - 1);
  Printf.fprintf outchan "|]"

let () =
  let l = [ 1; 2; 3; 4 ] and arr = [| 1; 2; 4 |] in
  Printf.printf "%a %a\n" pp_int_list l pp_int_array arr
