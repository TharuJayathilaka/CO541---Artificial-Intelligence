'''
Unit tests for eight.py

@author: kvlinden
@version 2feb2013

@modified-by: trbandara
'''

from search import Node
from eight import EightPuzzle
import unittest

class TestEight(unittest.TestCase):
    
    def setUp(self):
        self.problem = EightPuzzle("012345678", "012345678");
    
    def test_actions(self):
        self.assertEqual(self.problem.actions("012345678"), ["d", "r"])
        self.assertEqual(self.problem.actions("102345678"), ["d", "l", "r"])
        self.assertEqual(self.problem.actions("120345678"), ["d", "l"])
        self.assertEqual(self.problem.actions("123045678"), ["u", "d", "r"])
        self.assertEqual(self.problem.actions("123405678"), ["u", "d", "l", "r"])
        self.assertEqual(self.problem.actions("123450678"), ["u", "d", "l"])
        self.assertEqual(self.problem.actions("123456078"), ["u", "r"])
        self.assertEqual(self.problem.actions("123456708"), ["u", "l", "r"])
        self.assertEqual(self.problem.actions("123456780"), ["u", "l"])
    

    def test_result(self):
        self.assertEqual(self.problem.result("012345678", "r"), "102345678")
        self.assertEqual(self.problem.result("012345678", "d"), "312045678")
        self.assertEqual(self.problem.result("123405678", "u"), "103425678")
        self.assertEqual(self.problem.result("123405678", "d"), "123475608")
        self.assertEqual(self.problem.result("123405678", "l"), "123045678")
        self.assertEqual(self.problem.result("123405678", "r"), "123450678")
        self.assertEqual(self.problem.result("123456708", "u"), "123406758")
        self.assertEqual(self.problem.result("123456708", "l"), "123456078")
        self.assertEqual(self.problem.result("123456708", "r"), "123456780")
        
    def test_goal_test(self):
        self.assertTrue(self.problem.goal_test("012345678"))
        self.assertFalse(self.problem.goal_test("123456780"))
        self.assertTrue(self.problem.goal_test("".join("012345678")))
        
    def test_h_mismatched_tiles(self):
        self.assertEqual(self.problem.h_mismatched_tiles(Node("012345678")), 0)
        self.assertEqual(self.problem.h_mismatched_tiles(Node("120345678")), 2)
        self.assertEqual(self.problem.h_mismatched_tiles(Node("123405678")), 4)
        self.assertEqual(self.problem.h_mismatched_tiles(Node("724506831")), 8) # Text example, Figure 3.28

    def test_h_manhatten_distance(self):
        self.assertEqual(self.problem.h_manhattan_distance(Node("012345678")), 0)
        self.assertEqual(self.problem.h_manhattan_distance(Node("120345678")), 2)
        self.assertEqual(self.problem.h_manhattan_distance(Node("123405678")), 6)
        self.assertEqual(self.problem.h_manhattan_distance(Node("724506831")), 18) # Text example, Figure 3.28
        
        
if __name__ == "__main__":
    unittest.main()