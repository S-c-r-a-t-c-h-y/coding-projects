type color = 
  | Black 
  | White

type pieces = 
  | Pawn of color
  | Knight of color
  | Bishop of color
  | Rook of color
  | Queen of color
  | King of color

(* 
010 - pawn
011 - knight
100 - bishop
101 - rook
110 - queen
001 - king
8 - white
16 - black
*)

(* let piece_to_int piece = match piece with
  | 

let black_bishop = Bishop Black;;

let print_piece piece = let upper = ref false in let value = ref ' ' in 
  match piece with
  | Pawn color -> upper : *)

(* let print_fen =   *)