(* let creer n = Array.make n (Array.make n 0);;

   let placer x y l c elm = if (x=c)&&(y=l) then 2 else if (x=c)||(y=l)||(x-c=y-l)||(x-c=l-y) then 1 else elm;;

   let placer_reine x y plateau = Array.mapi (fun iy line -> Array.mapi (fun ix elm -> placer x y iy ix elm) line) plateau;;

   let afficher plateau = Array.map (fun line -> begin Array.map (fun x -> if x=2 then print_string "|R|" else (Printf.printf "|%d|" x)) line;print_endline ""; end) plateau

   let rec backtracking x line plateau n =
     if (x=n)||(line =n) then []
     else if (plateau.(line).(x) = 0) then let res = (backtracking 0 (line + 1) (placer_reine x line plateau) n) in
       if (res <> [])||(line = n-1) then (x::res) else backtracking (x+1) line plateau n
     else backtracking (x+1) line plateau n;;

   let solution n =
     let rec aux plateau liste x =
       match liste with
       |[] -> plateau
       |e::q -> aux (placer_reine x e plateau) q (x+1)
     in afficher (aux (creer n) (backtracking 0 0 (creer n) n) 0);;

   solution 25;; *)

(* let () = let print_solution n = let indices_valides reines ligne n = let rec cases_prises reines ligne n arr = match reines with | [] -> arr | e::q -> let (x, y) = e in arr.(x) <- 1; if (x + ligne - y) < n then arr.(x + ligne - y) <- 1; if (x - ligne + y) >= 0 then arr.(x - ligne + y) <- 1; cases_prises q ligne n arr in let range n = let rec aux i n = if i = n then [] else i :: aux (i + 1) n in aux 0 n in let arr = cases_prises reines ligne n (Array.make n 0) in List.filteri (fun i _ -> arr.(i) = 0) (range n) in let n_reines n = let rec i_reines i reines = let indices = (indices_valides reines i n) and k = ref 0 in if indices = [] then [] else if i = (n-1) then (List.hd indices, i)::reines else try while (i_reines (i+1) ((List.nth indices !k, i)::reines)) = [] do k := !k + 1 done; i_reines (i+1) ((List.nth indices !k, i)::reines) with _ -> [] in i_reines 0 [] in let rec flatten sol = match sol with | [] -> [] | e::q -> let (x, y) = e in x::(flatten q) in let sol = Array.of_list (List.rev (flatten (n_reines n))) in for i = 0 to (n-1) do for j = 0 to (n-1) do if j = sol.(i) then Printf.printf "|x" else Printf.printf "| "done; Printf.printf "|\n" done in if Array.length Sys.argv = 1 then print_solution 8 else let n = int_of_string Sys.argv.(1) in if n <= 3 then Printf.printf "Pas de solution pour n=%d" n else print_solution n;; *)

(* let affiche tab n =
     for k = 0 to n-1 do
       for i = 0 to n-1 do
         Printf.printf "|%c" tab.(k).(i);
       done;
       Printf.printf "|\n";
     done;;

   let reines n =
     let tableau = Array.make_matrix n n ' ' in
     let y = ref 0 in
     if n mod 2 = 0 then
       for i = 0 to n do
         if n = (i*6) then
           y := 6;
         if n = ((i*6)+2) then
           y := 8;
         if n = ((i*6)+4) then
           y := 10;
       done;
     if !y = 6 || !y = 10 then begin
       let gauche = if n mod 2 = 0 then ref ((n/2)-1) else ref (n/2) in
       let ecart = n/2 in
       for k = 0 to n-1 do
         if k mod 2 = 0 then
           tableau.(k).(!gauche) <- 'X'
         else begin
           tableau.(k).((!gauche)+ecart) <- 'X';
           gauche := (!gauche)-1
         end
       done;
     end;
     if !y = 8 || !y = 0 then begin
       let gauche = if n mod 2 = 0 then ref ((n/2)-1) else ref (n/2) in
       let ecart = n/2 in
       for k = 0 to n-1 do
         if k mod 2 = 0 then
           tableau.(k).(!gauche+ecart) <- 'X'
         else begin
           if !y = 8 then begin
             tableau.(k).(!gauche) <- 'X';
             gauche := (!gauche)-1;
           end
           else
             begin
               tableau.(k).((!gauche)-1) <- 'X';
               gauche := (!gauche)-1
             end
         end;
       done;
       if !y = 8 then begin
         tableau.(n-1).(0) <- ' ';
         tableau.(3).(0) <- 'X';
         tableau.(0).(n-1) <- ' ';
         tableau.(n-4).(n-1) <- 'X';
         tableau.(n-4).((n/2)+1) <- ' ';
         tableau.(0).((n/2)+1) <- 'X';
         tableau.(3).((n/2)-2) <- ' ';
         tableau.(n-1).((n/2)-2) <- 'X';
       end;
     end;
     affiche tableau n;;

     reines 9;; *)

let rec remove_isomorphismes sols =
  let isomorphismes sol =
    let n = List.length sol in
    List.map
      (fun x -> List.sort (fun (x1, y1) (x2, y2) -> y1 - y2) x)
      [
        List.map (fun (x, y) -> (n - x - 1, y)) sol;
        List.map (fun (x, y) -> (x, n - y - 1)) sol;
        List.map (fun (x, y) -> (y, x)) sol;
        List.map (fun (x, y) -> (n - y - 1, n - x - 1)) sol;
        List.map (fun (x, y) -> (n - y - 1, x)) sol;
        List.map (fun (x, y) -> (y, n - x - 1)) sol;
        List.map (fun (x, y) -> (n - x - 1, n - y - 1)) sol;
      ]
  in
  match sols with
  | [] -> []
  | e :: q ->
      let iso = isomorphismes e in
      e :: remove_isomorphismes (List.filter (fun x -> not (List.mem x iso)) q)

(* -------------------------- fonctions d'aide pour la résolution classique -------------------------- *)

let rec cases_prises reines ligne n arr =
  match reines with
  | [] -> arr
  | (x, y) :: q ->
      (* On récupère la position de la première reine dans la liste. *)
      arr.(x) <- 1;
      (* On marque la colonne correspondante de l'échiquier comme étant menacée. *)
      if x + ligne - y < n then arr.(x + ligne - y) <- 1;
      (* On marque la diagonale ascendante correspondante de l'échiquier comme étant menacée. *)
      if x - ligne + y >= 0 then arr.(x - ligne + y) <- 1;
      (* On marque la diagonale descendante correspondante de l'échiquier comme étant menacée. *)
      cases_prises q ligne n arr

(* On appelle récursivement la fonction pour les reines restantes dans la liste. *)

let indices_valides reines ligne n =
  let range n = List.init n (fun i -> i) in
  (* Crée une liste de 0 à n-1 *)
  let prises = cases_prises reines ligne n (Array.make n 0) in
  (* Calcule les cases menacées par les reines déjà placées *)
  Array.of_list (List.filteri (fun i _ -> prises.(i) = 0) (range n))

(* Filtre les indices des cases qui ne sont pas menacées *)

(* -------------------------- résolution pour UNE solution (méthode classique) -------------------------- *)

let nb_solutions n =
  let rec i_reines i reines =
    let indices = indices_valides reines i n in
    if Array.length indices = 0 then 0
    else if i = n - 1 then Array.length indices
    else
      let nb = ref (i_reines (i + 1) ((indices.(0), i) :: reines)) in
      for k = 1 to Array.length indices - 1 do
        nb := !nb + i_reines (i + 1) ((indices.(k), i) :: reines)
      done;
      !nb
  in
  i_reines 0 []

let solution n =
  let rec i_reines i reines =
    let indices = indices_valides reines i n and k = ref 0 in
    if Array.length indices = 0 then []
      (* cas de base : aucune colonne valide pour la ligne actuelle *)
    else if i = n - 1 then
      (indices.(0), i)
      :: reines (* cas de base : toutes les reines ont été placées *)
    else
      try
        let sol = ref (i_reines (i + 1) ((indices.(!k), i) :: reines)) in
        (* appel récursif pour la ligne suivante *)
        while !sol = [] do
          (* si l'appel récursif ne renvoie pas de solution, essayer la prochaine colonne valide *)
          k := !k + 1;
          sol := i_reines (i + 1) ((indices.(!k), i) :: reines)
        done;
        !sol (* si l'appel récursif renvoie une solution, la renvoyer *)
      with _ -> []
    (* si l'appel récursif provoque une exception, essayer la prochaine colonne valide *)
  in
  i_reines 0 []

(* appel initial avec i=0 et une liste vide de positions de reines *)

(* let solutions n all =
   let exception Fini in
   let sols = ref [] in
   let rec i_reines i reines =
     let indices = indices_valides reines i n in
     if i = n - 1 then (
       sols :=
         !sols
         @ List.init (Array.length indices) (fun x -> (indices.(x), i) :: reines);
       if (not all) && !sols <> [] then raise Fini)
     else Array.iter (fun x -> i_reines (i + 1) ((x, i) :: reines)) indices
   in
   try
     i_reines 0 [];
     !sols
   with Fini -> [ List.hd !sols ] *)

(* let solutions n =
   let rec i_reines i reines =
     let indices = indices_valides reines i n in
     if i = n - 1 then
       List.init (Array.length indices) (fun x -> [ (indices.(x), i) ])
     else
       let rec aux debut =
         if Array.length indices = debut then [ [] ]
         else
           let sol = ref (i_reines (i + 1) ((indices.(debut), i) :: reines)) in
           if !sol = [ [] ] then aux (debut + 1)
           else
             List.append
               (aux (debut + 1))
               (List.map (fun x -> (indices.(debut), i) :: x) !sol)
       in
       aux 0
   in
   List.filter (fun x -> List.length x = n) (i_reines 0 []) *)

let solutions n unique =
  (* On crée une variable mutable "sols" qui va contenir toutes les solutions*)
  let sols = ref [] in
  let rec i_reines i reines =
    (* On calcule les indices valides pour la "i"-ème ligne *)
    let indices = indices_valides reines i n in
    (* Si "i" est égal à "n-1", on ajoute toutes les solutions correspondantes à la liste "sols" *)
    if i = n - 1 then
      for j = 0 to Array.length indices - 1 do
        sols := ((indices.(j), i) :: reines) :: !sols
      done
      (* Sinon, pour chaque indice valide "x" pour la "i"-ème ligne, on appelle récursivement la fonction "i_reines" pour la "i+1"-ème ligne avec une nouvelle liste de reines qui contient le couple "(x, i)" ajouté à la liste "reines" *)
    else Array.iter (fun x -> i_reines (i + 1) ((x, i) :: reines)) indices
  in
  i_reines 0 [];
  (* On retourne la liste de toutes les solutions stockées dans la variable mutable "sols" *)
  if unique then remove_isomorphismes !sols else !sols

(*
   o3 : 27.954119s
   o2 : 27.530993s
   o1 : 27.913042s
*)

let psolutions n chan =
  let print_sol sol =
    let x, y = List.split sol in
    let sol = Array.of_list (List.rev x) in
    for i = 0 to n - 1 do
      for j = 0 to n - 1 do
        if j = sol.(i) then Printf.fprintf chan "|x"
        else Printf.fprintf chan "| "
      done;
      Printf.fprintf chan "|\n"
    done;
    Printf.fprintf chan "%s\n" (String.make ((2 * n) + 1) '-')
  in
  let rec i_reines i reines =
    let indices = indices_valides reines i n in
    if i = n - 1 then
      List.iter print_sol
        (List.init (Array.length indices) (fun x -> (indices.(x), i) :: reines))
    else Array.iter (fun x -> i_reines (i + 1) ((x, i) :: reines)) indices
  in
  Printf.fprintf chan "%s\n" (String.make ((2 * n) + 1) '-');
  i_reines 0 []

let print_solution n =
  let x, y = List.split (solution n) in
  let sol = Array.of_list (List.rev x) in
  for i = 0 to n - 1 do
    for j = 0 to n - 1 do
      if j = sol.(i) then Printf.printf "|x" else Printf.printf "| "
    done;
    Printf.printf "|\n"
  done

let print_solutions n unique in_file =
  let open_file file =
    open_out_gen [ Open_append; Open_creat; Open_trunc ] 0o666 file
  in
  let out_channel =
    if in_file then open_file (Printf.sprintf "out%d.txt" n) else stdout
  in
  let rec print_solution solutions =
    match solutions with
    | [] -> ()
    | e :: q ->
        let x, y = List.split e in
        let sol = Array.of_list x in
        for i = 0 to n - 1 do
          for j = 0 to n - 1 do
            if j = sol.(i) then Printf.fprintf out_channel "|x"
            else Printf.fprintf out_channel "| "
          done;
          Printf.fprintf out_channel "|\n"
        done;
        Printf.fprintf out_channel "%s\n" (String.make ((2 * n) + 1) '-');
        print_solution q
  in
  Printf.fprintf out_channel "%s\n" (String.make ((2 * n) + 1) '-');
  print_solution (solutions n unique)

let nb_solutions n = List.length (solutions n false);;

let start_time = Sys.time () in
(* psolutions 14
   (open_out_gen [ Open_append; Open_creat; Open_trunc ] 0o666 "out.txt"); *)
print_int (nb_solutions 15);
print_newline ();
Printf.printf "Temps d'exécution : %fs\n" (Sys.time () -. start_time)
(* print_int (nb_solutions 13) *)
(* print_mean_time 10 25;; *)
