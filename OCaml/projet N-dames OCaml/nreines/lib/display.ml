open Algorithm

(**
   [print_solution n] affiche dans [out_chan] le plateau d'échec de [n*n] avec les [n] reines placées au bon endroit.
   @param n        taille de l'échiquier
   @param out_chan channel de sortie sur lequel doit être affiché la solution (stdout ou un fichier)
*)
let print_solution n out_chan =
  (* on calcul une solution au problème et on sépare les coordonnées x et y des reines*)
  let x, _ = List.split (solution n) in
  (* on converti les coordonées x en un array pour itérer dessus et afficher les reines *)
  let sol = Array.of_list (List.rev x) in
  for i = 0 to n - 1 do
    for j = 0 to n - 1 do
      if j = sol.(i) then Printf.fprintf out_chan "|x"
      else Printf.fprintf out_chan "| "
    done;
    Printf.fprintf out_chan "|\n"
  done

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
        let x, _ = List.split e in
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

(**
    [print_solution_conflits n] affiche dans [out_chan] une solution au problème des n-reines obtenue à l'aide d'un algorithme de résolution de conflits
    @param n          la taille de l'échiquier
    @param iter_max   nombre d'itération maximale à effectuer sur un plateau
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