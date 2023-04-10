(**
  {1 Compte rendu}
  Pour la documentation globale du projet voir {{:compte_rendu.html}le compte rendu}.
*)

(**
  {1 Documentation du code}
  Ci-dessous la documentation pour toutes les fonctions du code.
*)

type reine = int * int
(**
une reine est représentée par un couple de coordonées [(i, j)]
*)

(** 
[cases_prises reines ligne n arr] calcul les cases de la ligne [ligne] pouvant être attaquées par une des reines de [reines] déjà placées
@param reines une liste des coordonnées des reines déjà placées sur le plateau
@param ligne  ligne pour laquelle on souhaite obtenir les indices des cases prises
@param n      nombre de reines
@param arr    array contenant n nombres, tous initialement à 0
@return un array de [n] nombres valant [1] si une
reine de [reines] peut attaquer la case à la position [(i, ligne)] où [i] est l'indice dans l'array, et [0] sinon.
*)
let rec cases_prises (reines : reine list) ligne n arr =
  match reines with
  | [] -> arr
  (* On récupère la position de la première reine dans la liste. *)
  | (x, y) :: q ->
      (* On marque la colonne correspondante de l'échiquier comme étant menacée. *)
      arr.(x) <- 1;
      (* On marque la diagonale ascendante correspondante de l'échiquier comme étant menacée. *)
      if x + ligne - y < n then arr.(x + ligne - y) <- 1;
      (* On marque la diagonale descendante correspondante de l'échiquier comme étant menacée. *)
      if x - ligne + y >= 0 then arr.(x - ligne + y) <- 1;
      (* On appelle récursivement la fonction pour les reines restantes dans la liste. *)
      cases_prises q ligne n arr

(** 
  [indices_valides reines ligne n] calcul les indices des cases sur lesquels on peut poser une reine sur la ligne [ligne] sans que celle ci ne puisse être attaquée par
  une reine de [reines]
   @param reines une liste des coordonnées des reines déjà placées sur le plateau
   @param ligne  ligne pour laquelle on souhaite obtenir les indices valides
   @param n      nombre de reines
   @return un array de tous ces indices
*)
let indices_valides reines ligne n =
  (* Crée une liste de 0 à n-1 *)
  let range n = List.init n (fun i -> i) in
  (* Calcule les cases menacées par les reines déjà placées *)
  let prises = cases_prises reines ligne n (Array.make n 0) in
  (* Filtre les indices des cases qui ne sont pas menacées *)
  List.filteri (fun i _ -> prises.(i) = 0) (range n) |> Array.of_list

(** {2 Résolution pour UNE solution (méthode classique)} *)

(**
  [solution n] calcul une solution au problème des n-reines pour un plateau de [n*n].
  @param n taille de l'échiquier
  @return une liste contenant les coordonnées des [n] reines
*)
let solution n =
  let rec i_reines i reines =
    let indices = indices_valides reines i n and k = ref 0 in
    (* cas de base : aucune colonne valide pour la ligne actuelle *)
    if Array.length indices = 0 then []
      (* cas de base : toutes les reines ont été placées *)
    else if i = n - 1 then (indices.(0), i) :: reines
    else
      try
        (* appel récursif pour la ligne suivante *)
        let sol = ref (i_reines (i + 1) ((indices.(!k), i) :: reines)) in
        (* si l'appel récursif ne renvoie pas de solution, essayer la prochaine colonne valide *)
        while !sol = [] do
          k := !k + 1;
          sol := i_reines (i + 1) ((indices.(!k), i) :: reines)
        done;
        (* si l'appel récursif renvoie une solution, la renvoyer *)
        !sol
        (* si l'appel récursif provoque une exception, essayer la prochaine colonne valide *)
      with _ -> []
  in
  i_reines 0
    [] (* appel initial avec i=0 et une liste vide de positions de reines *)

(**
   [print_solution n] affiche dans [out_chan] le plateau d'échec de [n*n] avec les [n] reines placées au bon endroit.
   @param n        taille de l'échiquier
   @param out_chan channel de sortie sur lequel doit être affiché la solution (stdout ou un fichier)
*)
let print_solution n out_chan =
  (* on calcul une solution au problème et on sépare les coordonnées x et y des reines*)
  let x, y = List.split (solution n) in
  (* on converti les coordonées x en un array pour itérer dessus et afficher les reines *)
  let sol = Array.of_list (List.rev x) in
  for i = 0 to n - 1 do
    for j = 0 to n - 1 do
      if j = sol.(i) then Printf.fprintf out_chan "|x"
      else Printf.fprintf out_chan "| "
    done;
    Printf.fprintf out_chan "|\n"
  done

(** {2 Résolution pour TOUTES les solutions} *)

(**
  [remove_isomorphismes sols] supprime toutes les solutions isomorphes à d'autres solutions, ne laissant que les solutions de "base"
  @param sols la liste de toutes les solutions
  @return la liste des solutions uniques à isomorphisme près
*)
let rec remove_isomorphismes (sols : reine list list) =
  (* renvoie une liste de tous les isomorphismes induit par la solution [sol] *)
  let isomorphismes sol =
    (* on détermine le nombre de reines *)
    let n = List.length sol in
    List.map
      (* on trie les reines en fonction de leurs coordonées y *)
        (fun x -> List.sort (fun (_, y1) (_, y2) -> y2 - y1) x)
      (* toutes les transformations possibles, à savoir symétries axiales et rotations *)
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
      (* on effectue un appel récursif sur le reste des solutions où tous les isomorphismes de [e] ont été filtrés *)
      e :: remove_isomorphismes (List.filter (fun x -> not (List.mem x iso)) q)

(**
    [solutions n unique] renvoie une liste de toutes les solutions pour un plateau de [n*n], uniques à isomorphisme près si [unique=true].
    @param n       taille de l'échiquier
    @param unique  si oui ou non les solutions renvoyées sont uniques
*)
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

(**
  [print_nb_solutions n unique out_chan] affiche dans [out_chan] le nombre de solutions pour un plateau de [n*n], uniques à isomorphisme près si [unique=true].
  @param n          taille de l'échiquier
  @param unique     si oui ou non les solutions affichées sont uniques
  @param out_chan   channel de sortie sur lequel doit être affiché la solution (stdout ou un fichier)
*)
let print_nb_solutions n unique out_chan =
  solutions n unique |> List.length
  |> Printf.fprintf out_chan "Nombre de solutions pour n=%d : %d\n" n

(**
   [print_solutions n unique out_chan] affiche dans [out_chan] toutes les configurations possibles de [n] reines sur un plateau de [n*n],
   uniques à isomorphisme près si [unique=true].
   @param n          taille de l'échiquier
   @param unique     si oui ou non les solutions affichées sont uniques
   @param out_chan   channel de sortie sur lequel doit être affiché la solution (stdout ou un fichier)
*)
let print_solutions n unique out_chan =
  let rec print_solution solutions =
    match solutions with
    | [] -> ()
    | e :: q ->
        let x, y = List.split e in
        let sol = Array.of_list x in
        for i = 0 to n - 1 do
          for j = 0 to n - 1 do
            if j = sol.(i) then Printf.fprintf out_chan "|x"
            else Printf.fprintf out_chan "| "
          done;
          Printf.fprintf out_chan "|\n"
        done;
        Printf.fprintf out_chan "%s\n" (String.make ((2 * n) + 1) '-');
        print_solution q
  in
  Printf.fprintf out_chan "%s\n" (String.make ((2 * n) + 1) '-');
  solutions n unique |> print_solution

(** {2 Résolution pour UNE solution (méthode de résolution de conflits)} *)

(**
    [place_n_reines n] place [n] reines aléatoirement sur un plateau de [n*n], une par ligne
    @param n nombre de reines à placer
    @return  un array des positions des [n] reines
*)
let place_n_reines n =
  let reines = Array.make n 0 in
  for i = 0 to n - 1 do
    reines.(i) <- Random.int n
  done;
  reines

(**
    [indice_min arr] renvoie l'indice d'un élément dont la valeur est le minimum de [arr]
    @param arr l'array d'entiers
    @return    l'indice de l'élément
*)
let indice_min (arr : int array) =
  let m = ref arr.(0) and inds = ref [ 0 ] in
  for i = 1 to Array.length arr - 1 do
    if arr.(i) < !m then (
      m := arr.(i);
      inds := [ i ])
    else if arr.(i) = !m then inds := i :: !inds
  done;
  List.length !inds |> Random.int |> List.nth !inds

(**
    [max_conflits reines n] calcul quelle reine est en conflit avec le plus de [reines] de [reines]
    @param reines un array des positions des reines
    @param n      le nombre de reines
    @return       l'indice de la reine en conflit avec le plus de reines ainsi que ce nombre de conflits
*)
let max_conflits reines n =
  let tmp = ref 0
  and col = Array.make n 0
  and diag1 = Array.make (n + n) 0
  and diag2 = Array.make (n + n) 0
  and value = ref 0
  and m = ref 0
  and inds = ref [ 0 ] in
  for i = 0 to n - 1 do
    value := reines.(i);
    col.(!value) <- col.(!value) + 1;
    diag1.(!value + i) <- diag1.(!value + i) + 1;
    diag2.(n - !value + i) <- diag2.(n - !value + i) + 1
  done;
  for i = 0 to n - 1 do
    value := reines.(i);
    tmp := col.(!value) + diag1.(!value + i) + diag2.(n - !value + i) - 3;
    if !tmp > !m then (
      m := !tmp;
      inds := [ i ])
    else if !tmp = !m then inds := i :: !inds
  done;
  (List.length !inds |> Random.int |> List.nth !inds, !m)

(**
    [calc_conflits_ligne reines ligne n] calcul les conflits de chaque cases de la ligne [ligne] avec les [reines]
    @param reines un array des positions des reines
    @param ligne  la ligne sur laquel chercher le nombre de conflit minimum
    @param n      le nombre de reines
    @return       un array où [array.(i)] contient le nombre de conflits entre les [reines] et la case d'indice (ligne, i)
*)
let calc_conflits_ligne reines ligne n =
  let conflits = Array.make n 0 and tmp = ref 0 in
  for i = 0 to n - 1 do
    if i <> ligne then (
      conflits.(reines.(i)) <- conflits.(reines.(i)) + 1;
      tmp := reines.(i) - i + ligne;
      if 0 <= !tmp && !tmp < n then conflits.(!tmp) <- conflits.(!tmp) + 1;
      tmp := reines.(i) + i - ligne;
      if 0 <= !tmp && !tmp < n then conflits.(!tmp) <- conflits.(!tmp) + 1)
  done;
  conflits

(**
    [min_conflits reines ligne n] cherche la colonne la moins en conflit avec les autres [reines] sur la ligne [ligne]
    @param reines un array des positions des reines
    @param ligne  la ligne sur laquel chercher le nombre de conflit minimum
    @param n      le nombre de reines
    @return       l'indice de la colonne la moins en conflit
*)
let min_conflits reines ligne n =
  calc_conflits_ligne reines ligne n |> indice_min

(**
    [reparer reines n] "répare" les [reines], c'est à dire qu'il déplace une reine dans l'optique de réduire le nombre de conflits total
    @param reines un array des positions des reines
    @param n      le nombre de reines
    @return       [true] si et seulement si aucune reine n'est en conflit après la réparation
*)
let reparer reines n =
  let ligne, nb_conflits = max_conflits reines n in
  reines.(ligne) <- min_conflits reines ligne n;
  nb_conflits <> 0

(**
    [solution_conflits n] résoud le problème des n-reines en utilisant une méthode de résolution de conflits
    @param  n la taille de l'échiquier
    @return un array où le nombre à l'index i représente l'ordonnée j de la reine sur la ligne i
*)
let solution_conflits n ?(iter_max = 2 * n) () =
  let reines = ref (place_n_reines n) and iter_count = ref 0 in
  while reparer !reines n do
    incr iter_count;
    if !iter_count = iter_max then (
      reines := place_n_reines n;
      iter_count := 0)
  done;
  !reines

(**
    [print_solution_conflits n] affiche dans [out_chan] une solution au problème des n-reines obtenue à l'aide d'un algorithme de résolution de conflits
    @param n          la taille de l'échiquier
    @param out_chan   channel de sortie sur lequel doit être affiché la solution (stdout ou un fichier)
*)
let print_solution_conflits n ?(iter_max = n) out_chan =
  let sol = solution_conflits n ~iter_max () in
  for i = 0 to n - 1 do
    for j = 0 to n - 1 do
      if j = sol.(i) then Printf.fprintf out_chan "|x"
      else Printf.fprintf out_chan "| "
    done;
    Printf.fprintf out_chan "|\n"
  done

(** {2 Programme principale} *)

(**
  [n_reines n all unique conflit nb out_chan print] détermine quelle fonction appeler en fonction des paramètres passés par l'utilisateur.
  Pour plus de précision sur les paramètres, exécutez [./n_reines --help]
*)
let n_reines n all unique conflit nb out_chan print =
  if n <= 0 || n = 2 || n = 3 then Printf.printf "Pas de solution pour n=%d\n" n
  else if print then
    if nb then print_nb_solutions n unique out_chan
    else if all || unique then print_solutions n unique out_chan
    else if conflit then print_solution_conflits n out_chan
    else print_solution n out_chan
  else if nb then solutions n unique |> List.length |> ignore
  else if all || unique then solutions n unique |> ignore
  else if conflit then solution_conflits n () |> ignore
  else solution n |> ignore

(**
    Fonction [main], pour obtenir des infos sur l'exécution du programme exécutez [./n_reines --help]
*)
let main =
  (* le fonctionnement de la fonction main n'est pas important, il permet d'exécuter le fichier avec différentes options *)
  let start_time = Sys.time () in
  let all = ref false in
  let unique = ref false in
  let conflit = ref false in
  let n = ref 8 in
  let out_chan = ref stdout in
  let print = ref true in
  let nb = ref false in
  let set_out_channel file =
    out_chan := open_out_gen [ Open_append; Open_creat; Open_trunc ] 0o666 file
  in
  let speclist : (Arg.key * Arg.spec * Arg.doc) list =
    Arg.align
      [
        ( "-all",
          Arg.Set all,
          " Affiche toutes les possibilités. Si l'option -unique est utilisée, \
           alors elle prend le dessus" );
        ( "-unique",
          Arg.Set unique,
          " Affiche toutes les possibilités uniques à isomorphisme près" );
        ( "-conflit",
          Arg.Set conflit,
          " Résolution à l'aide de la méthode de résolution des conflits (plus \
           lent). Incompatible avec les options -all et -unique" );
        ( "-nb",
          Arg.Set nb,
          " Renvoie uniquement le nombre de solutions et non les solutions \
           elles-même. Compatible avec -unique" );
        ( "-perf",
          Arg.Clear print,
          " Désactive l'affichage de tout résultat, pratique pour tester les \
           performances du programme" );
        ( "-o",
          Arg.String set_out_channel,
          "<fichier> Redirige la sortie du programme dans le fichier précisé \
           en paramètre. Si le fichier n'existe pas, il sera créé. ATTENTION : \
           l'écriture écrasera le contenu du fichier" );
        ("-n", Arg.Set_int n, "<int> Fixe le nombre de reines (défault=8)");
      ]
  in
  let usage_msg =
    "n_reines [-all] [-unique] [-conflit] [-nb] [-perf] [-o <nom du fichier>] \
     [-n <nombre de reines>]"
  in
  Arg.parse speclist (fun anon -> ()) usage_msg;
  Random.self_init ();
  n_reines !n !all !unique !conflit !nb !out_chan !print;
  Printf.printf "Temps d'exécution : %fs\n" (Sys.time () -. start_time)

let () = main
