(* Dans toutes les spécifications, n >= 4 *)

(*---------------------------------------------------------------------*)
(*-----------------------------Affichage-------------------------------*)
(*---------------------------------------------------------------------*)

(* Entrée : pos, un vecteur de taille n
            n, la taille de la matrice et du vecteur
Sortie : une matrice de taille n par n (l'échiquier)
Type : int array -> int -> int array array
But : Génère un échiquier à partir d'un vecteur contenant les positions des reines *)
let gen_board pos n =
  let board = ref (Array.make_matrix n n 0); in
  for i = 0 to (n-1) do
    for j = 0 to (n-1) do
      if i=pos.(j) then !board.(i).(j) <- 1 (* A partir d'une position, pour une colonne j fixé, si la ligne est celle où la j-ième reine doit se situer, on attribue 1*)
      else !board.(i).(j) <- 0; (* Sinon, il n'y a pas de reine : c'est un 0 *)
    done;
  done;
  !board;;

(* Entrée : board, une matrice de taille n par n
            n, la taille de la matrice
Sortie : ne renvoie rien
Type : int array array -> int -> unit
But : Affiche la matrice *)
let print_board board n =
  print_newline ();
  Printf.printf "Plateau :";
  print_newline ();
  for i = 0 to (n-1) do (* On itère sur chaque ligne / chaque colonne et on affiche la valeur de la case : 1 <-> une reine ; 0 <-> rien *)
    for j = 0 to (n-1) do
      if board.(i).(j) = 1 then print_string "|x" else print_string "| "
    done;
    Printf.printf "|\n";
  done;;

(* Entrée : pos, un vecteur de taille n
            n, la taille du vecteur
Sortie : ne renvoie rien
Type : int array -> int -> unit
But : Affiche le vecteur *)
let print_pos pos n = 
  print_newline ();
  Printf.printf "Etat :";
  print_newline ();
  for i = 0 to (n-1) do (* On itère sur chaque elt du vecteur *)
    Printf.printf "%d " (pos.(i));
  done;
  print_newline ();;

(*---------------------------------------------------------------------*)
(*-------------------------Isomorphismes-------------------------------*)
(*---------------------------------------------------------------------*)

(* Entrée : board, une matrice de taille nxn
            n, la taille de la matrice
Sortie : board avec une rotation de 90°
Type : int array array -> int -> int array array
But : Faire une rotation de 90° à la matrice *)
let rotate90 board n = 
  let tmp = ref (0); in
  for i = 0 to ((n/2)-1) do
    for j = i to (n-i-2) do (* On échange les valeurs pour faire une rotation de 90° *)
      tmp := board.(i).(j);
      board.(i).(j) <- board.(j).(n-1-i);
      board.(j).(n-1-i) <- board.(n-1-i).(n-1-j);
      board.(n-1-i).(n-1-j) <- board.(n-1-j).(i);
      board.(n-1-j).(i) <- !tmp;
    done;
  done;
  board;;
  
(* Entrée : board, une matrice de taille nxn
            n, la taille de la matrice
Sortie : board avec une transposition
Type : int array array -> int -> int array array
But : Faire une transposition à la matrice *)
let transposition board n = 
  let tmp = ref (0); in
  for i = 0 to (n-1) do
    for j = i to (n-1) do (* On échange ij et ji*)
      tmp := board.(i).(j);
      board.(i).(j) <- board.(j).(i);
      board.(j).(i) <- !tmp;
    done;
  done;
  board;;

(*---------------------------------------------------------------------*)
(*-----------------------------Utils-----------------------------------*)
(*---------------------------------------------------------------------*)

(* Entrée : pos1, un vecteur de taille n
            pos2, un vecteur de taille n
            n, la taille des vecteurs
Sortie : pos1, le vecteur de taille n désormais égal à pos2
Type : 'a array -> 'a array -> int -> 'a array
But : Copie le vecteur pos2 dans le vecteur pos1 *)
let copy pos1 pos2 n =
  for i = 0 to (n-1) do
    pos1.(i) <- pos2.(i); (* On copie les valeurs de pos2 dans pos1 : de préférence, pos1 est un échiquier vide sinon la fonction n'a pas d'intérêt *)
  done;
  pos1;;

(* Entrée : pos, un vecteur de taille n
            n, la taille de la matrice et du vecteur
Sortie : un vecteur de taille n contenant la position des reines
Type : int array -> int -> int array
But : Génère un échiquier aléatoirement *)
let gen_random pos n = 
  Random.self_init (); (* Initialisation nécessaire pour ne pas toujours retomber sur la même configuration ; pour plus de détail, se renseigner sur *)
  for i = 0 to (n-1) do                         (* la fonction random en Ocaml (docs) et sur la génération de nombres aléatoires, il y a bcp d'articles en ligne *)
    pos.(i) <- (Random.int 1000) mod n; (* On attribue à pos[i] une valeur comprise entre 0 et n-1 *)
  done;
  pos;;

(*---------------------------------------------------------------------*)
(*--------------------------Hill-Climbing------------------------------*)
(*---------------------------------------------------------------------*)

(*Entrée : pos, un vecteur de taille n
           n, la taille de la matrice et du vecteur
Sortie : un entier représentant le nombre de conflits sur l'échiquier
Type : int array -> int -> int
But : Calculer le nombre de conflits sur un échiquier*)
let calc_conflicts pos n =
  let row = ref (Array.make n 0); in
  let diag1 = ref (Array.make (n+n) 0); in
  let diag2 = ref (Array.make (n+n) 0); in
  let value = ref (0); in
  let conf = ref (0); in
  for i = 0 to (n-1) do
    value := pos.(i);
    !row.(!value) <- (!row.(!value) + 1); (* On marque qu'il y a une reine sur la ligne value <-> pos.(i) *)
    !diag1.(!value + i) <- (!diag1.(!value + i) + 1); (* Pareil pour la première diag, mais cette fois ci il y a 2N-1 cases*)
    !diag2.(n - !value + i) <- (!diag2.(n - !value + i) + 1); (* Parei pour la seconde diag, mais ...*)
  done;
  for i = 0 to (2*n - 1) do (* sur une ligne (resp diag1, diag2), s'il y a x dames, alors il y a clairement x-1 conflits *)
    if (i < n) && (!row.(i) <> 0) then conf := !conf + (!row.(i) - 1); (* A noter que les lignes / diags ne provoquent pas de conflts*)
    if !diag1.(i) <> 0 then conf := !conf + (!diag1.(i) - 1); (* directement entre elles, donc pas de souci de ce pt de vue là *)
    if !diag2.(i) <> 0 then conf := !conf + (!diag2.(i) - 1);
  done;
  !conf;; (* on renvoie le résultat *)


(*Entrée : pos, un vecteur de taille n
           n, la taille de la matrice et du vecteur
Sortie : la position voisine comportant le moins de conflits
Type : int array -> int -> int array
But : Renvoie la position minimisant les conflits sur la planche*)
let next pos n =
  let opti_pos = ref (Array.make n 0); in (* pos (vecteur) *)
  let opti_obj = ref 0; in (* conflits (int) *)
  let neighbour_pos = ref (Array.make n 0); in
  let temp = ref 0; in (* conflits temp (int) *)

  (* on définit la position opti *)
  opti_pos := copy (!opti_pos) pos n;
  opti_obj := calc_conflicts (!opti_pos) n;

  (* on définit le voisin *)
  neighbour_pos := copy (!neighbour_pos) pos n;

  (* on parcourt toutes les possibilités de voisins (cf pdf pour les explications) et on essaie de minimiser l'objectif *)
  for i = 0 to (n-1) do
    for j = 0 to (n-1) do
      if (j <> pos.(i)) then begin (* bien entendu, ça ne sert à rien de considérer l'échiquier actuel *)
        (* on étudie ce voisin : on le définit dans neighbour_pos en bougeant la reine *)
        !neighbour_pos.(i) <- j;

        (* calcule des conflits *)
        temp := calc_conflicts (!neighbour_pos) n;

        (* dans le cas où la position est meilleure, on actualise l'objectif à battre et la position opti *)
        if !temp <= !opti_obj then begin
          opti_obj := !temp;
          opti_pos := copy (!opti_pos) (!neighbour_pos) n;
        end;

        (* on reset la position à l'état précédent *)
        (!neighbour_pos).(i) <- pos.(i);
      end;
    done;
  done;
  (* on renvoie la position optimale *)
  (ref pos) := copy pos !opti_pos n;
  pos;;
  
(*Entrée : pos, un vecteur de taille n
           n, la taille de la matrice et du vecteur
Sortie : Rien
Type : int array -> int -> int array
But : Renvoie une solution au problème des N-reines*)
let hill_climbing pos n =
  (* l'idée est mieux développée dans le pdf : très utile pour comprendre le code *)
  let neighbour_pos = ref (Array.make n 0); in
  let tmp_bool = ref true; in
  neighbour_pos := copy (!neighbour_pos) pos n;

  while !tmp_bool do
    (ref pos) := copy pos (!neighbour_pos) n;

    (* on détermine le voisin le plus opti *)
    neighbour_pos := next !neighbour_pos n;

    if (calc_conflicts pos n) = 0 then begin (* s'il est optimal, cad qu'il n'y a pas de conflits, on sort du while et on print la planche*)
      tmp_bool := false;
    end
    else if (calc_conflicts pos n) = (calc_conflicts !neighbour_pos n) then begin (* sinon, si l'on s'approche d'un extrema local / d'un plateau *)
      !neighbour_pos.((Random.int 1000) mod n) <- (Random.int 1000) mod n;                    (* <-> le mm nombre de conflits mais une position différente *)
    end
  done;
  pos;;

(*---------------------------------------------------------------------*)
(*------------------------------Driver---------------------------------*)
(*---------------------------------------------------------------------*)

let main1 n=
  let objBoard = ref (0); in
  let pos1 = ref (Array.make n 0); in
  let tp = ref 0.; in
  let t = ref (Sys.time()); in
  pos1 := gen_random !pos1 n; (* on initialise *)
  pos1 := hill_climbing !pos1 n; (* on calcule la solution *)
  tp := Sys.time(); (* On stop le tps ici pour ne pas perdre de tps avec l'affichage *)
  print_board (gen_board !pos1 n) n;
  Printf.printf "\nExecution time: %fs seconde(s)\n" ((!tp -. !t));
  objBoard := calc_conflicts !pos1 n; (* permet de vérifier qu'il n'y a pas de conflits : la fonction calc_conflicts est correcte *)
  Printf.printf "Nombres de conflits : %d. " !objBoard;
  if !objBoard = 0 then Printf.printf "Planche correcte.\n"
  else Printf.printf "Planche incorrecte.\n";;

let main2 n=
  for i = 10 to 10 do
    let t = ref (Sys.time()); in
    let tp = ref 0.; in
    for j = 1 to 20 do (* Modifier le nombre d'itérations ici => modifier le float_of_int à la fin de la fct *)
      let pos1 = ref (Array.make i 0); in
      pos1 := gen_random !pos1 i; (* on initialise *)
      pos1 := hill_climbing !pos1 i; (* on calcule la solution *)
    done;
    tp := Sys.time(); (* On stop le tps ici pour ne pas perdre de tps avec l'affichage *)
    Printf.printf ("\nExecution time for N = %d : %fs \n") i ((!tp -. !t)/.float_of_int(20)); (* Prq ocaml n'écrit le texte qu'à la fin de l'exécution et pas pendant ? *)
  done;;



let main3 n =
  let pos1 = ref (Array.make n 0); in
  pos1 := gen_random !pos1 n; (* on initialise *)
  pos1 := hill_climbing !pos1 n; (* on calcule la solution *)
  Printf.printf ("\nIdentité : "); (* cf printf pour comprendre l'opération *)
  print_board (gen_board !pos1 n) n;
  Printf.printf ("\nRotation de 90° : ");
  print_board (rotate90 (gen_board !pos1 n) n) n;
  Printf.printf ("\nRotation de 180° : ");
  print_board (rotate90 (rotate90 (gen_board !pos1 n) n) n) n;
  Printf.printf ("\nRotation de 270° : ");
  print_board (rotate90 (rotate90 (rotate90 (gen_board !pos1 n) n) n) n) n;
  Printf.printf ("\nSymétrie par rapport à l'axe horizontal : ");
  print_board (rotate90 (transposition (gen_board !pos1 n) n) n) n;
  Printf.printf ("\nSymétrie par rapport à l'axe vertical : ");
  print_board (transposition (rotate90 (gen_board !pos1 n) n) n) n;
  Printf.printf ("\nSymétrie par rapport à la première diagonale : ");
  print_board (transposition (gen_board !pos1 n) n) n;
  Printf.printf ("\nSymétrie par rapport à la seconde diagonale : ");
  print_board (transposition (rotate90 (rotate90 (gen_board !pos1 n) n) n) n) n;;

let main n i = 
  Printf.printf "%d" i;
  if i = 1 then main1 n
  else if i = 2 then main2 n
    else if i = 3 then main3 n;;
    
(* Appel *)
main (try int_of_string (Sys.argv.(1)) with _ -> 8) (try int_of_string (Sys.argv.(2)) with _ -> 1);;