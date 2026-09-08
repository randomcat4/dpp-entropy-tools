import Std

/- Exact integer identities for the fixed matrices in frozen A2 v2.
   This is only the matrix-algebra component, not the entropy theorem. -/
namespace A2

abbrev M4 := Fin 4 → Fin 4 → Int

def A : M4 := fun i j => match i.val, j.val with
  | 0, 1 | 1, 0 | 2, 3 | 3, 2 => 1
  | _, _ => 0

def B : M4 := fun i j => match i.val, j.val with
  | 0, 2 | 2, 0 => 1
  | 1, 3 | 3, 1 => -1
  | _, _ => 0

def ident : M4 := fun i j => if i = j then 1 else 0

def mul (X Y : M4) : M4 := fun i j =>
  X i 0 * Y 0 j + X i 1 * Y 1 j + X i 2 * Y 2 j + X i 3 * Y 3 j

theorem A_squared : ∀ i j : Fin 4, mul A A i j = ident i j := by decide
theorem B_squared : ∀ i j : Fin 4, mul B B i j = ident i j := by decide
theorem anticommutes : ∀ i j : Fin 4, mul A B i j = -(mul B A i j) := by decide
theorem product_nonzero : mul A B 0 3 = -1 := by decide
theorem noncommutes : mul A B ≠ mul B A := by
  intro heq
  have hentry : mul A B 0 3 ≠ mul B A 0 3 := by decide
  exact hentry (congrFun (congrFun heq 0) 3)

#print axioms A_squared
#print axioms B_squared
#print axioms anticommutes
#print axioms product_nonzero
#print axioms noncommutes

end A2
