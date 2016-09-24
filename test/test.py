import unittest

from app.data_mining import compute_gain,process_file

from app.data_processing import title_cleaning,fetch_listings_title_from_api,read_file


class DataProcessingTest(unittest.TestCase):
    def test_title_cleaning(self):
        self.assertEqual(title_cleaning("&i' am! )alpha-!numerique"), "i am alpha numerique")
        self.assertEqual(title_cleaning("multiple     space"), "multiple space")
        self.assertEqual(title_cleaning("LOWERcase"),'lowercase')

    def test_fetch_listings_titles_from_api(self):
        fetch_listings_title_from_api([179324107])
        self.assertEqual(fetch_listings_title_from_api([179324107]),["plum purple wool acrylic aplaca slippers house home shoes warm knitted winter quality women slippers housewarming birthday christmas gifts"])

    def test_read_file(self):
        file_name = 'test/test.txt'
        with open(file_name,'w') as f:
            f.write("a\nb\nc")
        self.assertEqual(read_file(file_name),["a","b","c"])


class DataMiningTest(unittest.TestCase):
    def test_data_mining(self):
        # Small test to see if the information gain is coherent
        a = [{1} for e in range(10)]+[{3} for e in range(10)]
        b = [{2} for e in range(10)]+[{3} for e in range(10)]
        testab = compute_gain(a,b)
        self.assertAlmostEqual(testab[0][1],testab[1][1])
        self.assertGreater(testab[1][1],testab[2][1])

    def test_process_file(self):
        file_name = 'test/test.txt'
        with open(file_name,'w') as f:
            f.write("a\nb\nc")
        self.assertEqual(process_file(file_name),[{"a"},{"b"},{"c"}])




if __name__ == '__main__':
    unittest.main()
