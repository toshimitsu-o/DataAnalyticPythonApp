from search import Search
import unittest

class TestCases(unittest.TestCase):

    def test_hourly_average(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('00', 0.162291169451074), ('01', 0.09785202863961814), ('02', 0.09069212410501193), ('03', 0.08591885441527446), ('04', 0.0883054892601432), ('05', 0.19331742243436753), ('06', 0.5871121718377088), ('07', 1.1336515513126493), ('08', 1.79236276849642), ('09', 1.4391408114558473), ('10', 1.1909307875894988), ('11', 1.3436754176610979), ('12', 1.4176610978520285), ('13', 1.4367541766109786), ('14', 1.4343675417661097), ('15', 1.9498806682577565), ('16', 2.1503579952267304), ('17', 2.3484486873508352), ('18', 1.9236276849642004), ('19', 0.9976133651551312), ('20', 0.60381861575179), ('21', 0.5847255369928401), ('22', 0.477326968973747), ('23', 0.28162291169451076)]
        actual = x.hourly_average()
        self.assertEqual(expected, actual)

    def test_hourly_averageType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.hourly_average()
        actual = type(x.hourly_average())
        self.assertIsInstance(expected, list)

    def test_getDateRange(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = ('2013-07-01', '2019-03-21')
        actual = x.getDateRange()
        self.assertEqual(expected, actual)

    def test_getDateRangeType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.getDateRange()
        actual = type(x.getDateRange())
        self.assertIsInstance(expected, tuple)

    def test_getTotalDays(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = (419,)
        actual = x.getTotalDays()
        self.assertEqual(expected, actual)

    def test_getTotalDaysType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.getTotalDays()
        actual = type(x.getTotalDays())
        self.assertIsInstance(expected, tuple)

    def test_listAccidentType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = ['Struck Pedestrian', 'Collision with vehicle', 'Collision with a fixed object', 'No collision and no object struck', 'Struck animal', 'Vehicle overturned (no collision)', 'collision with some other object', 'Fall from or in moving vehicle', 'Other accident']
        actual = x.listAccidentType()
        self.assertEqual(expected, actual)

    def test_listAccidentTypeType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.listAccidentType()
        actual = type(x.listAccidentType())
        self.assertIsInstance(expected, list)

    def test_accidentTypeList(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('Collision with vehicle', 9977)]
        actual = x.accidentTypeList()
        self.assertEqual(expected, actual)

    def test_accidentTypeListType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.accidentTypeList()
        actual = type(x.accidentTypeList())
        self.assertIsInstance(expected, list)

    def test_accidentTypeListAlcohol(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [[('Collision with vehicle', 184)], [('Collision with vehicle', 9793)]]
        actual = x.accidentTypeList(mode= 'alcohol')
        self.assertEqual(expected, actual)

    def test_accidentTypeListTypeAlcohol(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.accidentTypeList(mode='alcohol')
        actual = type(x.accidentTypeList(mode='alcohol'))
        self.assertIsInstance(expected, list)

    def test_calcAllAccidentType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = []
        actual = x.calcAllAccidentType()
        self.assertEqual(expected, actual)

    def test_calcAllAccidentTypeType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calcAllAccidentType()
        actual = type(x.calcAllAccidentType())
        self.assertIsInstance(expected, list)

    def test_calcAllAccidentTypeAlcohol(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [[], [('Collision with vehicle', 184)]]
        actual = x.calcAllAccidentType(mode='alcohol')
        self.assertEqual(expected, actual)

    def test_calcAllAccidentTypeTypeAlcohol(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calcAllAccidentType(mode='alcohol')
        actual = type(x.calcAllAccidentType(mode='alcohol'))
        self.assertIsInstance(expected, list)

    def test_calculate_by_month(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('01', 632), ('02', 729), ('03', 840), ('04', 725), ('05', 829), ('06', 739), ('07', 1361), ('08', 1233), ('09', 696), ('10', 778), ('11', 694), ('12', 721)]
        actual = x.calculate_by_month()
        self.assertEqual(expected, actual)

    def test_calculate_by_monthType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calculate_by_month()
        actual = type(x.calculate_by_month())
        self.assertIsInstance(expected, list)

    def test_calculate_by_monthAlcohol(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [[('01', 10), ('02', 11), ('03', 13), ('04', 12), ('05', 17), ('06', 7), ('07', 32), ('08', 22), ('09', 21), ('10', 14), ('11', 9), ('12', 16)], [('01', 622), ('02', 718), ('03', 827), ('04', 713), ('05', 812), ('06', 732), ('07', 1329), ('08', 1211), ('09', 675), ('10', 764), ('11', 685), ('12', 705)]]
        actual = x.calculate_by_month(mode='alcohol')
        self.assertEqual(expected, actual)

    def test_calculate_by_monthTypeAlcohol(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calculate_by_month(mode='alcohol')
        actual = type(x.calculate_by_month(mode='alcohol'))
        self.assertIsInstance(expected, list)

    def test_calculate_by_day(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('Monday', 1369), ('Tuesday', 1558), ('Wednesday', 1615), ('Thursday', 1587), ('Friday', 1566), ('Saturday', 1218), ('Sunday', 1013)]
        actual = x.calculate_by_day()
        self.assertEqual(expected, actual)

    def test_calculate_by_dayType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calculate_by_day()
        actual = type(x.calculate_by_day())
        self.assertIsInstance(expected, list)

    def test_listLGAS(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = ['MELBOURNE', 'WHITEHORSE', 'BRIMBANK', 'MITCHELL', 'BAW BAW', 'BAYSIDE', 'BOROONDARA', 'BANYULE', 'HUME', 'WHITTLESEA', 'GEELONG', 'HOBSONS BAY', 'NILLUMBIK', 'PORT PHILLIP', 'DAREBIN', 'YARRA', 'LATROBE', 'MOONEE VALLEY', 'KNOX', 'CASEY', 'BENDIGO', 'FRANKSTON', 'EAST GIPPSLAND', 'KINGSTON', 'MAROONDAH', 'BALLARAT', 'CAMPASPE', 'SHEPPARTON', 'MILDURA', 'DANDENONG', 'MONASH', 'GOLDEN PLAINS', 'MORNINGTON PENINSULA', 'WYNDHAM', 'CORANGAMITE', 'BASS COAST', 'MURRINDINDI', 'STONNINGTON', 'MORELAND', 'MOORABOOL', 'YARRA RANGES', 'MARIBYRNONG', 'STRATHBOGIE', 'CARDINIA', 'TOWONG', 'WANGARATTA', 'MELTON', 'SURF COAST', 'SOUTH GIPPSLAND', 'HEPBURN', 'SOUTHERN GRAMPIANS', 'GLEN EIRA', 'BENALLA', 'MOYNE', 'COLAC OTWAY', 'MACEDON RANGES', 'MOIRA', 'WELLINGTON', 'WEST WIMMERA', 'MANSFIELD', 'LODDON', 'WODONGA', 'INDIGO', 'HORSHAM', 'MANNINGHAM', 'NORTHERN GRAMPIANS', 'PYRENEES', 'ALPINE', 'BULOKE', 'GANNAWARRA', 'ARARAT', 'WARRNAMBOOL', 'GLENELG', 'SWAN HILL', 'HINDMARSH', '(FALLS CREEK)', 'MOUNT ALEXANDER', 'CENTRAL GOLDFIELDS', '(MOUNT BULLER)', '(MOUNT HOTHAM)', 'YARRIAMBIACK', '(LAKE MOUNTAIN)', '(MOUNT BAW BAW)', 'QUEENSCLIFFE', 'MOUNT BULLER ALPINE RESOR', ' ', '(FRENCH ISLAND)', '(MOUNT STIRLING)']
        actual = x.listLgas()
        self.assertEqual(expected, actual)

    def test_listLGASType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.listLgas()
        actual = type(x.listLgas())
        self.assertIsInstance(expected, list)

    def test_calcAllLGAS(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('WHITEHORSE', 245), ('MELBOURNE', 652), ('BAYSIDE', 144), ('BOROONDARA', 301), ('WHITTLESEA', 306), ('BANYULE', 153), ('HOBSONS BAY', 170), ('PORT PHILLIP', 256), ('DAREBIN', 275), ('MOONEE VALLEY', 193), ('KNOX', 242), ('CASEY', 424), ('FRANKSTON', 200), ('KINGSTON', 330), ('MAROONDAH', 185), ('BALLARAT', 213), ('CAMPASPE', 46), ('SHEPPARTON', 88), ('MILDURA', 66), ('HUME', 354), ('DANDENONG', 385), ('MONASH', 382), ('MORNINGTON PENINSULA', 193), ('YARRA', 282), ('BAW BAW', 63), ('GEELONG', 381), ('WYNDHAM', 280), ('MURRINDINDI', 18), ('STONNINGTON', 265), ('MORELAND', 331), ('MOORABOOL', 36), ('BRIMBANK', 402), ('YARRA RANGES', 213), ('MARIBYRNONG', 168), ('LATROBE', 95), ('SURF COAST', 38), ('CARDINIA', 95), ('HEPBURN', 10), ('SOUTHERN GRAMPIANS', 13), ('GLEN EIRA', 251), ('CORANGAMITE', 23), ('COLAC OTWAY', 33), ('GOLDEN PLAINS', 21), ('BASS COAST', 36), ('MITCHELL', 44), ('MELTON', 167), ('EAST GIPPSLAND', 47), ('WEST WIMMERA', 5), ('WELLINGTON', 56), ('BENDIGO', 157), ('LODDON', 11), ('WODONGA', 36), ('HORSHAM', 32), ('MANNINGHAM', 120), ('MOIRA', 28), ('ALPINE', 12), ('MOYNE', 31), ('STRATHBOGIE', 9), ('GANNAWARRA', 6), ('INDIGO', 19), ('SOUTH GIPPSLAND', 32), ('WARRNAMBOOL', 36), ('NILLUMBIK', 68), ('MANSFIELD', 13), ('SWAN HILL', 28), ('WANGARATTA', 29), ('GLENELG', 15), ('PYRENEES', 7), ('ARARAT', 13), ('(FALLS CREEK)', 2), ('MOUNT ALEXANDER', 17), ('BENALLA', 11), ('NORTHERN GRAMPIANS', 9), ('CENTRAL GOLDFIELDS', 12), ('MACEDON RANGES', 34), ('HINDMARSH', 4), ('(MOUNT HOTHAM)', 2), ('BULOKE', 3), ('TOWONG', 4), ('QUEENSCLIFFE', 1)]
        actual = x.calcAllLgas()
        self.assertEqual(expected, actual)

    def test_calcAllLGASType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calcAllLgas()
        actual = type(x.calcAllLgas())
        self.assertIsInstance(expected, list)

    def test_calcLGA(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('BAYSIDE', 144)]
        actual = x.calculateLGA()
        self.assertEqual(expected, actual)

    def test_calcLGAType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calculateLGA()
        actual = type(x.calculateLGA())
        self.assertIsInstance(expected, list)

    def test_listRegions(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = ['METROPOLITAN NORTH WEST REGION', 'METROPOLITAN SOUTH EAST REGION', 'NORTHERN REGION', 'EASTERN REGION', 'SOUTH WESTERN REGION', 'WESTERN REGION', 'NORTH EASTERN REGION', ' ']
        actual = x.listRegions()
        self.assertEqual(expected, actual)

    def test_listRegionsType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.listRegions()
        actual = type(x.listRegions())
        self.assertIsInstance(expected, list)

    def test_matchRegions(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = ['EASTERN REGION', 'NORTH EASTERN REGION']
        actual = x.matchRegions()
        self.assertEqual(expected, actual)

    def test_matchRegionsType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.matchRegions()
        actual = type(x.matchRegions())
        self.assertIsInstance(expected, list)
    def test_CalcAllRegions(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('METROPOLITAN SOUTH EAST REGION', 3946), ('METROPOLITAN NORTH WEST REGION', 4086), ('WESTERN REGION', 407), ('NORTHERN REGION', 346), ('NORTH EASTERN REGION', 271), ('EASTERN REGION', 329), ('SOUTH WESTERN REGION', 592)]
        actual = x.calcAllRegions()
        self.assertEqual(expected, actual)

    def test_calcAllRegionsType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calcAllRegions()
        actual = type(x.calcAllRegions())
        self.assertIsInstance(expected, list)

    def test_calculate_region(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = [('NORTH EASTERN REGION', 271), ('EASTERN REGION', 329)]
        actual = x.calculate_region()
        self.assertEqual(expected, actual)

    def test_calculate_regionType(self):
        x = Search(To_Date = "2014-08-23", From_Date = "2013-07-01", Accident_Type_List="Collision with vehicle", Lga= "BAYSIDE", Region= 'EASTERN REGION')
        expected = x.calculate_region()
        actual = type(x.calculate_region())
        self.assertIsInstance(expected, list)

    

    

    

    

    

    

    

    

    

    




        




if __name__ == '__main__':
    unittest.main()
    