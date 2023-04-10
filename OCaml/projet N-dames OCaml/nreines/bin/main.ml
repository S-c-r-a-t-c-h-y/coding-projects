(** {2 Programme principale} *)

open Nreines
open Display
open Algorithm

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
          " Résolution à l'aide de la méthode de résolution des conflits. \
           Incompatible avec les options -all et -unique" );
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
  Arg.parse speclist (fun _ -> ()) usage_msg;
  Random.self_init ();
  n_reines !n !all !unique !conflit !nb !out_chan !print;
  Printf.printf "Temps d'exécution : %fs\n" (Sys.time () -. start_time)

let () = main
