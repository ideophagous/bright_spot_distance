import unittest
import bright_spot_distance as bsd
from math import sqrt
#from PIL import Image

class distance_test_module(unittest.TestCase):
    def setUp(self):
        #the test cases were generated using the following tool:
        #https://www.favicon-generator.org/image-editor/
        self.images = ["images/spot1.jpg","images/spot2.jpg","images/spot3.jpg","images/spot4.jpg","images/spot5.jpg"]
        self.coordinate_sets = [[(457,520),(230,412),(463,520),(937,607)],
                                            [(162,141),(203,53),(227,62)],[(102,121),(448,276),(1651,1663)]]
        self.neighborhoods = [[],[(14,20)],[(10,105),(11,104),(14,100)]]
        self.pixel_list1 = [(0,10),(457,520),(0,15),(230,412),(461,520),
                                                                (937,607),(930,605),(1,14),(1007,954)]
        self.pixel_list2 = [(100,15),(12,1025)]
        self.pixel_list3 = [(54,36)]
        self.pixel_list4 = [(1,2),(3,4),(5,6),(7,8),(9,10),(19,13)]
        self.empty_list = []
    def test_get_image(self):
        #for image "spot1.jpg"
        #for coordinates = (457,520)
        self.assertAlmostEqual(bsd.get_image(self.images[0]).getpixel(
                                                            self.coordinate_sets[0][0]),12,delta=1)
        #for coordinates = (230,412)
        self.assertAlmostEqual(bsd.get_image(self.images[0]).getpixel(
                                                            self.coordinate_sets[0][1]),1,delta=1)
        #for coordinates = (463,520)
        self.assertAlmostEqual(bsd.get_image(self.images[0]).getpixel(
                                                            self.coordinate_sets[0][2]),11,delta=1)
        #for coordinates = (937,607)
        self.assertAlmostEqual(bsd.get_image(self.images[0]).getpixel(
                                                            self.coordinate_sets[0][3]),0,delta=1)
        #for image "spot2.jpg"
        #for coordinates = (162,141)
        self.assertAlmostEqual(bsd.get_image(self.images[1]).getpixel(
                                                            self.coordinate_sets[1][0]),2,delta=1)
        #for coordinates = (203,53)
        self.assertAlmostEqual(bsd.get_image(self.images[1]).getpixel(
                                                            self.coordinate_sets[1][1]),254,delta=1)
        #for coordinates = (227,62)
        self.assertAlmostEqual(bsd.get_image(self.images[1]).getpixel(
                                                            self.coordinate_sets[1][2]),6,delta=1)
        #for image "spot3.jpg"
        #for coordinates = (102,121)
        self.assertAlmostEqual(bsd.get_image(self.images[2]).getpixel(
                                                            self.coordinate_sets[2][0]),0,delta=1)
        #for coordinates = (448,276)
        self.assertAlmostEqual(bsd.get_image(self.images[2]).getpixel(
                                                            self.coordinate_sets[2][1]),2,delta=1)
        #for coordinates = (1651,1663)
        self.assertAlmostEqual(bsd.get_image(self.images[2]).getpixel(
                                                            self.coordinate_sets[2][2]),238,delta=1)
        #for image "spot4.jpg" - this file or image doesn't exist
        self.assertEqual(bsd.get_image(self.images[3]),None)
        #for image "spot5.jpg" - there's a file with this name, but it's not an image
        self.assertEqual(bsd.get_image(self.images[4]),None)
        
    def test_get_brightness_threshold(self):
        #for image "spot1.jpg"
        self.assertEqual(bsd.get_brightness_threshold(bsd.get_image(self.images[0])),2)
        #for image "spot2.jpg"
        self.assertEqual(bsd.get_brightness_threshold(bsd.get_image(self.images[1])),41)
        #for image "spot3.jpg"
        self.assertEqual(bsd.get_brightness_threshold(bsd.get_image(self.images[2])),25)
        #for image "spot4.jpg" - this file or image doesn't exist
        self.assertEqual(bsd.get_brightness_threshold(bsd.get_image("spot4.jpg")),None)

    #this unit test takes around 18 seconds to execute on my machine
    def test_get_bright_pixel_list(self):
        #for image "spot1.jpg"
        self.assertTrue((457,520) in bsd.get_bright_pixel_list(bsd.get_image(self.images[0])))
        self.assertTrue((230,412) not in bsd.get_bright_pixel_list(bsd.get_image(self.images[0])))
        #for image "spot2.jpg"
        self.assertTrue((203,53) in bsd.get_bright_pixel_list(bsd.get_image(self.images[1])))
        self.assertTrue((162,141) not in bsd.get_bright_pixel_list(bsd.get_image(self.images[1])))
        #for image "spot3.jpg"
        self.assertTrue((1651,1663) in bsd.get_bright_pixel_list(bsd.get_image(self.images[2])))
        self.assertTrue((102,121) not in bsd.get_bright_pixel_list(bsd.get_image(self.images[2])))
        #for image "spot4.jpg" - this file or image doesn't exist
        self.assertEqual(bsd.get_bright_pixel_list(bsd.get_image(self.images[3])),None)
        pass
        
    def test_check_neighboring_pixel(self):
        self.assertFalse(bsd.check_neighboring_pixel(self.neighborhoods[0],(0,0)))
        self.assertFalse(bsd.check_neighboring_pixel(self.neighborhoods[1],(0,0)))
        self.assertTrue(bsd.check_neighboring_pixel(self.neighborhoods[1],(10,23)))
        self.assertFalse(bsd.check_neighboring_pixel(self.neighborhoods[1],(15,100)))
        self.assertFalse(bsd.check_neighboring_pixel(self.neighborhoods[1],(63,22)))
        self.assertFalse(bsd.check_neighboring_pixel(self.neighborhoods[2],(7,95)))
        self.assertTrue(bsd.check_neighboring_pixel(self.neighborhoods[2],(6,101)))
        self.assertFalse(bsd.check_neighboring_pixel(self.neighborhoods[2],(102,10)))

    def test_get_neighborhood_list(self):
        self.assertEqual(len(bsd.get_neighborhood_list(self.neighborhoods[0])),0)
        self.assertEqual(len(bsd.get_neighborhood_list(self.neighborhoods[1])),1)
        self.assertEqual(len(bsd.get_neighborhood_list(self.neighborhoods[2]+[(1000,250)])),2)
        self.assertEqual(len(bsd.get_neighborhood_list(self.pixel_list1)),6)
        self.assertEqual(len(bsd.get_neighborhood_list(self.pixel_list2)),2)

    #this unit test takes around 18 seconds to execute on my machine    
    def test_get_bright_spot(self):
        #for image "spot1.jpg"
        self.assertTrue((457,520) in bsd.get_bright_spot(bsd.get_neighborhood_list(
                                        bsd.get_bright_pixel_list(bsd.get_image(self.images[0])))))
        self.assertTrue((230,412) not in bsd.get_bright_spot(bsd.get_neighborhood_list(
                                        bsd.get_bright_pixel_list(bsd.get_image(self.images[0])))))
        #for image "spot2.jpg"
        self.assertTrue((203,53) in bsd.get_bright_spot(bsd.get_neighborhood_list(
                                        bsd.get_bright_pixel_list(bsd.get_image(self.images[1])))))
        self.assertTrue((162,141) not in bsd.get_bright_spot(bsd.get_neighborhood_list(
                                        bsd.get_bright_pixel_list(bsd.get_image(self.images[1])))))
        #for image "spot3.jpg"
        self.assertTrue((1651,1663) in bsd.get_bright_spot(bsd.get_neighborhood_list(
                                        bsd.get_bright_pixel_list(bsd.get_image(self.images[2])))))
        self.assertTrue((102,121) not in bsd.get_bright_spot(bsd.get_neighborhood_list(
                                        bsd.get_bright_pixel_list(bsd.get_image(self.images[2])))))
        self.assertEqual(bsd.get_bright_spot([]),[])

    def test_get_bright_spot_center(self):
        self.assertEqual(bsd.get_bright_spot_center(self.pixel_list2),(56,520))
        self.assertEqual(bsd.get_bright_spot_center(self.pixel_list3),(54,36))
        self.assertAlmostEqual(bsd.get_bright_spot_center(self.pixel_list4),(44/6.0,43/6.0))
        self.assertEqual(bsd.get_bright_spot_center(self.empty_list),None)
        

    def test_get_image_center(self):
        #for image "spot1.jpg"
        self.assertEqual(bsd.get_image_center(bsd.get_image(self.images[0])),(539.5,539.5))
        #for image "spot2.jpg"
        self.assertEqual(bsd.get_image_center(bsd.get_image(self.images[1])),(134.5,134.5))
        #for image "spot3.jpg"
        self.assertEqual(bsd.get_image_center(bsd.get_image(self.images[2])),(1079.5,1079.5))
        #for image "spot4.jpg"
        self.assertEqual(bsd.get_image_center(bsd.get_image(self.images[3])),None)

    def test_get_distance_to_center(self):
        self.assertAlmostEqual(bsd.get_distance_to_center(self.pixel_list4[0],
                                                          self.pixel_list4[1]),2*sqrt(2))
        self.assertEqual(bsd.get_distance_to_center(self.pixel_list3[0],
                                                    self.pixel_list3[0]),0)
        self.assertAlmostEqual(bsd.get_distance_to_center(self.coordinate_sets[2][0],
                                                          self.coordinate_sets[2][2]),
                                                           sqrt((1549**2+1542**2)))
        self.assertEqual(bsd.get_distance_to_center(None,self.pixel_list3[0]),None)
        self.assertEqual(bsd.get_distance_to_center(self.pixel_list3[0],None),None)
        self.assertEqual(bsd.get_distance_to_center(None,None),None)
        
    

if __name__=='__main__':
    unittest.main()
