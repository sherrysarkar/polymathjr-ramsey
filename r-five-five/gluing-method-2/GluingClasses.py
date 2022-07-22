

# This file was *autogenerated* from the file GluingClasses.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2)### Defines Classes that will be used for Gluing via Method 2 from the R(5,5) paper


# Create an enum to represent the different values that a variable/PotentialEdge can take:
import enum
class EdgeExists(enum.Enum):
    UNKNOWN = _sage_const_0 
    TRUE = _sage_const_1 
    FALSE = _sage_const_2 



# Define a class to represent variables as described on page 7
class PotentialEdge:
    
    # Construct a new PotentialEdge between vertex G_vert in G and H_vert in H
    def __init__(self, G_vert, H_vert):
        # Set variables
        self.G_vertex = G_vert
        self.H_vertex = H_vert
        # Set current value of the variable
        exists = EdgeExists.UNKNOWN
        # Create sets of clique clauses and independent-set clauses
        self.clique_clauses = []
        self.ind_set_clauses = []
    
    
    # Set the value of the variable
    # NOTE: This should only be used when we change the value from UNKNOWN to TRUE or FALSE
    # INPUT: new_value for exists to be set to
    def set_exists(self, new_value):
        self.exists = new_value
        # Decrease the number of unknown for each clause this variable is in
        for clause in self.clique_clauses:
            clause.decr_num_unknown(new_value)
        for clause in self.ind_set_clauses:
            clause.decr_num_unknown(new_value)
    
    
    # Add a clause that the variable is in
    # INPUT: a clause that this variable is in and that should be added to it's list,
    #        a boolean that is true if the clause is a clique clause and false if it is an independent-set clause
    def add_clause(self, clause, clique_clause):
        if clique_clause:
            self.clique_clauses.append(clause)
        else:
            self.ind_set_clauses.append(clause)



# Define a class to represent clauses as described on page 7
class Clause:
    
    # Construct a new Clause
    # INPUT: a list of PotentialEdges/variables that are contained in this Clause
    #        a boolean that is True if the clause is a clique clause and False if it is an independent-set clause
    def __init__(self, variables, clique_clause):
        # Set variables
        self.potential_edges = variables
        self.num_unknown = len(variables)
        self.clique_clause = clique_clause
        # Number of variables whose value is undesired 
        #        (i.e. number of TRUEs if it's a clique clause, FALSEs if an independent set clause)
        self.num_undesired = _sage_const_0 
        
        # Add clauses to each potential edge
        for pot_edge in variables:
            pot_edge.add_clause(self, clique_clause)
    
    
    # Decrease the number of unknowns, called when a PotentialEdge's value goes from UNKNOWN to TRUE or FALSE
    # INPUT: the new value that the PotentialEdge was changed to
    def decr_num_unknown(self, new_value):
        # Decrease the number of unknowns by 1
        self.num_unknown -= _sage_const_1 
        # Update number of variables with undesired value
        if self.clique_clause and new_value == EdgeExists.TRUE:
            self.num_undesired += _sage_const_1 
        elif not self.clique_clause and new_value == EdgeExists.FALSE:
            self.num_undesired += _sage_const_1 
    
    
    # Determine whether all PotentialEdges in the clause are set to a value (i.e. are not UNKNOWN)
    # OUTPUT: a boolean, True if there are no UNKNOWNs, False otherwise
    def is_full(self):
        return self.num_unknown == _sage_const_0 
    
    # Determine whether the clique causes a FAIL state
    #       i.e. if all variables are TRUE when this is a clique clause or all variables FALSE when this is an independent set clause
    # OUTPUT: a boolean, True if in a FAIL state, False otherwise
    def in_fail_state(self):
        return self.num_unknown == _sage_const_0  and self.num_undesired == len(self.potential_edges)


# Construct a class to represent the matrix of variables
class PotentialEdgeMatrix:
    
    # Construct a new Matrix of Potential Edges as described in the paper
    # INPUT: num_rows = |VG|-|VK|-1, num_cols = |VH|-|VK|-1
    def __init__(self, num_rows, num_cols):
        # Create the matrix
        # NOTE: Should probably change to a more efficient data structure, since python lists are LinkedLists
        self.matrix = []
        for row in range(_sage_const_0 , num_rows):
            current_row = []
            for col in range(_sage_const_0 , num_cols):
                current_row.append(PotentialEdge(row, col))
            self.matrix.append(current_row)







# Some tests to make sure the classes are working as intended
testEdge1 = PotentialEdge(_sage_const_0 ,_sage_const_0 )
testEdge2 = PotentialEdge(_sage_const_0 ,_sage_const_1 )
testEdge3 = PotentialEdge(_sage_const_0 ,_sage_const_2 )
testClause1 = Clause([testEdge1, testEdge2], True)
testClause2 = Clause([testEdge1, testEdge3], False)

print("Clause 1 starts with %s unknowns" % (testClause1.num_unknown))
print("Clause 2 starts with %s unknowns" % (testClause2.num_unknown))

print("Setting first potential edge to FALSE")
testEdge1.set_exists(EdgeExists.FALSE)

print("Afterwards there are %s unknowns and %s undesired variables in Clause 1" 
      % (testClause1.num_unknown, testClause1.num_undesired))
print("Afterwards there are %s unknowns and %s undesired variables in Clause 2" 
      % (testClause2.num_unknown, testClause2.num_undesired))

print("Setting other two potential edges, should keep Clause 1 ok, but put Clause 2 into a FAIL state")
testEdge2.set_exists(EdgeExists.TRUE)
testEdge3.set_exists(EdgeExists.FALSE)

print("Afterwards there are %s unknowns and %s undesired variables in Clause 1" 
      % (testClause1.num_unknown, testClause1.num_undesired))
print("Afterwards there are %s unknowns and %s undesired variables in Clause 2" 
      % (testClause2.num_unknown, testClause2.num_undesired))
print("Is Clause 1 in a fail state? %s" % (testClause1.in_fail_state()))
print("Is Clause 2 in a fail state? %s" % (testClause2.in_fail_state()))
