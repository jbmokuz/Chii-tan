import unittest
from functions import *




class TestWaiting(unittest.TestCase):
    
    def setUp(self):
        self.gi = GameInstance()

    def testAddWaiting(self):
        self.gi.reset()
        self.assertEqual([str(i) for i in self.gi.waiting], [])
        self.assertEqual(self.gi.addWaiting("test"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["test"])
        self.assertEqual(self.gi.addWaiting("test"),1)        
        self.assertEqual([str(i) for i in self.gi.waiting], ["test"])
        self.assertEqual(self.gi.addWaiting("test2"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["test","test2"])        
        
    def testRemoveWaiting(self):
        self.gi.reset()
        self.assertEqual(self.gi.waiting, [])
        self.assertEqual(self.gi.addWaiting("test"),0)
        self.assertEqual(self.gi.removeWaiting("test"),0)
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("1")
        self.gi.addWaiting("2")
        self.assertEqual(self.gi.addWaiting("3"),0)
        self.assertEqual(self.gi.addWaiting("3"),1)
        self.gi.addWaiting("4")
        self.assertEqual(self.gi.removeWaiting("2"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","3","4"])
        self.assertEqual(self.gi.removeWaiting("3"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4"])
        self.assertEqual(self.gi.addWaiting("5"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4","5"])
        self.assertEqual(self.gi.removeWaiting("9"),1)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4","5"])

class TestGame(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testShuffle(self):
        self.gi.reset()
        self.assertFalse(self.gi.addWaiting("1"))
        self.gi.addWaiting("2")
        self.assertEqual(self.gi.shuffle(),{})
        self.assertEqual(self.gi.waiting,["1","2"])
        self.gi.addWaiting("3")
        self.gi.addWaiting("4")
        self.gi.addWaiting("5")
        self.gi.addWaiting("6")
        self.gi.addWaiting("7")
        self.gi.addWaiting("8")
        self.gi.addWaiting("9")
        ret1 = self.gi.shuffle()
        self.assertEqual(len(self.gi.waiting), 1)
        self.assertEqual(len(ret1[1]), 4)
        ret2 = self.gi.shuffle()
        self.assertEqual(ret2,{})
        self.gi.addWaiting("10")
        self.gi.addWaiting("11")
        self.gi.addWaiting("12")
        self.gi.addWaiting("13")
        ret3 = self.gi.shuffle(2)
        self.assertEqual(len(ret3),2)
        self.assertEqual(len(self.gi.waiting), 1)

class TestTourny(unittest.TestCase):
    
    def setUp(self):
        self.gi = GameInstance()

    def testReport(self):
        self.gi.reset()
        self.assertFalse(self.gi.report("Moku",25000))

    def testPlayer(self):
        self.gi.reset()
        self.assertFalse(self.gi.addPlayer("Moku"))
        self.assertFalse(self.gi.addPlayer("moku"))
        self.assertTrue(self.gi.addPlayer("Moku"))
        self.assertFalse(self.gi.removePlayer("Moku"))
        self.assertTrue(self.gi.removePlayer("Moku"))
        #self.gi.parseGame("http://tenhou.net/0/?log=2020061514gm-0209-19713-de5270f7&tw=0")
        self.assertFalse(self.gi.parseGame("https://tenhou.net/0/?log=2020061613gm-0209-19691-0508dda5&tw=1"))
        self.assertTrue(self.gi.parseGame("https://tenhou.net/0/?log=2020061613gm-0209-19691-0508dda5&tw=1"))
        self.assertTrue(self.gi.parseGame("https://tenhou.net/0/?log=2020061613gm-0209-19691-0508dda5"))

        self.assertTrue(self.gi.parseGame("https://tenhou.net/0/"))        
        #self.gi.parseGame("http://tenhou.net/0/?log=2020061809gm-0209-19691-ed012917&tw=3")
        #self.gi.parseGame("https://tenhou.net/0/?log=2020061613gm-0209-19691-2444973d&tw=3")
        #self.gi.parseGame("https://tenhou.net/0/?log=2020061612gm-0209-19691-4023b1f9&tw=3")
        #self.gi.parseGame("http://tenhou.net/0/?log=2020061514gm-0209-19713-5953946a&tw=0")

        
if __name__ == '__main__':
    unittest.main()
