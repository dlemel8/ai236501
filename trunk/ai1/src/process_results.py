import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import wilcoxon
from numpy.numarray.functions import average

def plot_simple_graph(title, x_lable, y_lable, grid,plt_func, *args):
	plt.figure()
	plt_func(*args)
	plt.xlabel(x_lable)
	plt.ylabel(y_lable)
	plt.title(title)
	#plt.axis([0, 100, 0, 2])
	plt.grid(grid)

def get_xys_info(list):
	xs = []
	ys = []
	rank = 0
	for x, y in list:
		xs.append(x)
		ys.append(y)
		rank += y
	return xs, ys, rank

runtime_of_dirts_dict = {'AStar': [(3, 0.49803208442336439), (4, 0.20217875328677404), (5, 0.13011688417672715), (6, 0.10348575547342313), (7, 0.1002876956070935), (8, 0.17673759545951739), (9, 0.26195869062485222), (10, 0.11242427524162898), (11, 0.090799767018330743), (12, 0.31678641824309511), (13, 0.37839872835271449), (14, 0.29256176671513501), (15, 0.27514893455399753), (16, 0.12183743434792405), (17, 0.070659493578286089), (18, 0.12931907070016516), (19, 0.55655642008262873), (20, 0.24439283923382932), (21, 0.29496795548853139), (22, 0.097855613982428161), (23, 0.16340614503810166), (24, 0.12088713771063435), (25, 0.11950877131751782), (26, 0.1701669789181772), (27, 0.15601595151714512), (28, 0.23930200471859767), (29, 0.12664232067098855), (30, 0.19102437169985934), (31, 0.093957700180976281), (32, 0.11434792982637987), (33, 0.079440938557345839), (34, 0.097125913859113164), (35, 0.11464341091125821), (36, 0.16490426802864672), (37, 0.17444219950457379), (38, 0.14261031414045833), (39, 0.2503199536657264), (40, 0.071104412527799352), (41, 0.10399011670967007), (42, 0.083780790176853137), (43, 0.079991583051117046), (44, 0.092839429800553763), (45, 0.14989883975815069), (46, 0.094111110964819472), (47, 0.093797473948704482), (48, 0.11757161057016437), (49, 0.10707833593598749), (50, 0.15180150887499394), (51, 0.089299352815246757), (52, 0.145625374307986), (53, 0.15290890207427524), (54, 0.13254341261967251), (55, 0.12359726086495315), (56, 1.0023390436674515), (57, 0.18622943449545465), (58, 0.59787750064241196), (59, 0.20052452153486305), (60, 0.089696231850138017), (61, 0.11375994343193195), (62, 0.11678434810369254), (63, 0.091020778895939194), (64, 0.082308723930999861), (65, 0.1159045414897194), (66, 0.1965349754718049), (67, 0.077506854231051511), (68, 0.10882594776129441), (69, 0.10853422518777035), (70, 0.16439200628990094), (71, 0.13175639699280303), (72, 0.11951609807122862), (73, 0.11124602679653547), (74, 0.11934176558402768), (75, 0.12651652510163938), (76, 0.13180081651736791), (77, 0.090609681694703875), (78, 0.14075254844622939), (79, 0.15957441217001303), (80, 0.077152583559637833), (81, 0.1911185582902879), (82, 0.10104824248106446), (83, 0.10225306712754627), (84, 0.20392002281601576), (85, 0.091637440917622159), (86, 0.14065401827008903), (87, 0.073334880067866981), (88, 0.093207709699948349), (89, 0.14280986712675114), (90, 0.079583503920235263), (91, 0.086965482782126541), (92, 0.11540890114270536), (93, 0.10265940505252964), (94, 0.077207210423307027), (95, 0.13604267127294695), (96, 0.16808018907387159), (97, 0.082097183462375364), (98, 0.094115441775937475), (99, 0.13094066693773845)], 'DirtsDivisionHeuristic': [(3, 0.80860842663075216), (4, 0.79581659043934327), (5, 0.29498039098945306), (6, 0.26811761197614992), (7, 0.17237957929439215), (8, 0.21584975715211785), (9, 0.19719064404203912), (10, 0.22793158685423834), (11, 0.18936087704356519), (12, 0.27612798217695556), (13, 0.14606133737506666), (14, 0.37871445516265012), (15, 0.44287039712630377), (16, 0.17982525756554679), (17, 0.12980060874175128), (18, 0.29830121395141634), (19, 0.18547307273150698), (20, 0.10284716879352089), (21, 0.23139749391905676), (22, 0.11672189397318339), (23, 0.155561067992877), (24, 0.10715492786419627), (25, 0.14816253229032442), (26, 0.14535710832505144), (27, 0.17089122428747686), (28, 0.3403362336548505), (29, 0.1737396970374295), (30, 0.21772420850101828), (31, 0.1833449729694489), (32, 0.18303969432424338), (33, 0.10073422758689572), (34, 0.1186622070811873), (35, 0.23327204791949854), (36, 0.13057726493068048), (37, 0.17068125513370322), (38, 0.25846929912580663), (39, 0.13593260457846176), (40, 0.064751539644794326), (41, 0.10647135466822087), (42, 0.2143681288083274), (43, 0.10766180714671368), (44, 0.15414055020945805), (45, 0.23953119953857063), (46, 0.10041011075721777), (47, 0.1423405466388929), (48, 0.10541062156021279), (49, 0.15830893360331702), (50, 0.091180764743712645), (51, 0.11210050423141424), (52, 0.19179988303251713), (53, 0.1294921488373339), (54, 0.12484380570093537), (55, 0.19385841431645656), (56, 0.11892890376293508), (57, 0.32331942341926279), (58, 0.20210187524719261), (59, 0.12395899050074018), (60, 0.10542411596065525), (61, 0.11876175754549258), (62, 0.51756114542496334), (63, 0.13137116054010928), (64, 0.097852164074115677), (65, 0.11349402273897514), (66, 0.12825310703272297), (67, 0.11403439376639408), (68, 0.26472231414734726), (69, 0.21224363456494888), (70, 0.1078339769707132), (71, 0.19325585305891699), (72, 0.096451066780474548), (73, 0.09636747344754365), (74, 0.11684064692498874), (75, 0.27085055868956565), (76, 0.12499195333482535), (77, 0.13861968726035098), (78, 0.091294114943745328), (79, 0.38782779211329638), (80, 0.12835902145365879), (81, 0.086978272515114127), (82, 0.12163441432457558), (83, 0.10495603060393566), (84, 0.18453553807334597), (85, 0.099161285587364117), (86, 0.087372933059007896), (87, 0.097061792563855651), (88, 0.09071839817496849), (89, 0.18701435404750555), (90, 0.11677283402255448), (91, 0.19818890082021906), (92, 0.10067895179477042), (93, 0.10714297047741062), (94, 0.096880531068399389), (95, 0.078142447976133081), (96, 0.079921554334229469), (97, 0.078942717493074396), (98, 0.10855169454596911), (99, 0.1345642144774134)], 'OneDirtPerRobotHeuristic': [(3, 0.49803208442336439), (4, 0.20217875328677404), (5, 0.13011688417672715), (6, 0.10348575547342313), (7, 0.1002876956070935), (8, 0.17673759545951739), (9, 0.26195869062485222), (10, 0.11242427524162898), (11, 0.090799767018330743), (12, 0.31678641824309511), (13, 0.37839872835271449), (14, 0.29256176671513501), (15, 0.27514893455399753), (16, 0.12183743434792405), (17, 0.070659493578286089), (18, 0.12931907070016516), (19, 0.55655642008262873), (20, 0.24439283923382932), (21, 0.29496795548853139), (22, 0.097855613982428161), (23, 0.16340614503810166), (24, 0.12088713771063435), (25, 0.11950877131751782), (26, 0.1701669789181772), (27, 0.15601595151714512), (28, 0.23930200471859767), (29, 0.12664232067098855), (30, 0.19102437169985934), (31, 0.093957700180976281), (32, 0.11434792982637987), (33, 0.079440938557345839), (34, 0.097125913859113164), (35, 0.11464341091125821), (36, 0.16490426802864672), (37, 0.17444219950457379), (38, 0.14261031414045833), (39, 0.2503199536657264), (40, 0.071104412527799352), (41, 0.10399011670967007), (42, 0.083780790176853137), (43, 0.079991583051117046), (44, 0.092839429800553763), (45, 0.14989883975815069), (46, 0.094111110964819472), (47, 0.093797473948704482), (48, 0.11757161057016437), (49, 0.10707833593598749), (50, 0.15180150887499394), (51, 0.089299352815246757), (52, 0.145625374307986), (53, 0.15290890207427524), (54, 0.13254341261967251), (55, 0.12359726086495315), (56, 1.0023390436674515), (57, 0.18622943449545465), (58, 0.59787750064241196), (59, 0.20052452153486305), (60, 0.089696231850138017), (61, 0.11375994343193195), (62, 0.11678434810369254), (63, 0.091020778895939194), (64, 0.082308723930999861), (65, 0.1159045414897194), (66, 0.1965349754718049), (67, 0.077506854231051511), (68, 0.10882594776129441), (69, 0.10853422518777035), (70, 0.16439200628990094), (71, 0.13175639699280303), (72, 0.11951609807122862), (73, 0.11124602679653547), (74, 0.11934176558402768), (75, 0.12651652510163938), (76, 0.13180081651736791), (77, 0.090609681694703875), (78, 0.14075254844622939), (79, 0.15957441217001303), (80, 0.077152583559637833), (81, 0.1911185582902879), (82, 0.10104824248106446), (83, 0.10225306712754627), (84, 0.20392002281601576), (85, 0.091637440917622159), (86, 0.14065401827008903), (87, 0.073334880067866981), (88, 0.093207709699948349), (89, 0.14280986712675114), (90, 0.079583503920235263), (91, 0.086965482782126541), (92, 0.11540890114270536), (93, 0.10265940505252964), (94, 0.077207210423307027), (95, 0.13604267127294695), (96, 0.16808018907387159), (97, 0.082097183462375364), (98, 0.094115441775937475), (99, 0.13094066693773845)], 'BeamSearch': [(3, 0.56952546074716281), (4, 0.31992776924344257), (5, 0.17089366891490662), (6, 0.15194677791356348), (7, 0.12692672359085627), (8, 0.21297750288835759), (9, 0.30522357762175922), (10, 0.18207698968198044), (11, 0.1383195448206723), (12, 0.27215468321135755), (13, 0.232052690877875), (14, 0.32894913491513983), (15, 0.13895850089058684), (16, 0.1428290649111883), (17, 0.092230205258095346), (18, 0.12879112812389337), (19, 0.1600221359943278), (20, 0.27123306057108182), (21, 0.3698263959589112), (22, 0.16364197680924389), (23, 0.20898867322816891), (24, 0.15487074289091041), (25, 0.22220722369156534), (26, 0.2669392512525563), (27, 0.19884008321390029), (28, 0.2481383226576952), (29, 0.14971691802341622), (30, 0.18430278303724398), (31, 0.10782643657644038), (32, 0.18329046883011557), (33, 0.092647463642963016), (34, 0.15158352229016381), (35, 0.12858566047431005), (36, 0.14631357502182457), (37, 0.23482058723256485), (38, 0.15231426142446031), (39, 0.22123149447706353), (40, 0.088142874520296746), (41, 0.14510358598260092), (42, 0.09090545477821993), (43, 0.11278220922754424), (44, 0.099159661826631537), (45, 0.20114449624355377), (46, 0.074437541525059187), (47, 0.092257886485807392), (48, 0.1163290992139115), (49, 0.1050720848970973), (50, 0.13154823672882229), (51, 0.10816515614421369), (52, 0.42994077756252014), (53, 0.17805454935794515), (54, 0.076048566953128713), (55, 0.12915991985527481), (56, 0.24856703031952471), (57, 0.27129908937368191), (58, 0.19421188315118343), (59, 0.14274637115712244), (60, 0.13947331547538699), (61, 0.170667307122531), (62, 0.1507811724292728), (63, 0.12014291505950798), (64, 0.11656039131280593), (65, 0.10736133543653242), (66, 0.16196676587938011), (67, 0.10987286200684343), (68, 0.12280367593959174), (69, 0.13510189441112216), (70, 0.15844351082053632), (71, 0.17042343955687986), (72, 0.12111618608922312), (73, 0.13540599496387237), (74, 0.21708969065999811), (75, 0.11459585489657002), (76, 0.10191317889372815), (77, 0.096311314873381501), (78, 0.20649097013220469), (79, 0.14091987253979099), (80, 0.085139855025229846), (81, 0.17840311829020744), (82, 0.12065394188988837), (83, 0.14091644215919444), (84, 0.16553094957391967), (85, 0.10155460021859493), (86, 0.17792629731583962), (87, 0.11474641119742245), (88, 0.086818642816917257), (89, 0.16543287684673866), (90, 0.12453510970684015), (91, 0.096379785296856244), (92, 0.17117471879112392), (93, 0.13621803699381554), (94, 0.09229949312088806), (95, 0.14085322501830791), (96, 0.15417341279760421), (97, 0.078871073067298264), (98, 0.093938708294393908), (99, 0.18868512920985406)]}
def process_runtime_of_dirt(key1, key2):
	print '### comparing runtime between', key1, 'and', key2, '###'
	k1_x, k1_y, k1_rank = get_xys_info(runtime_of_dirts_dict[key1])
	k2_x, k2_y, k2_rank = get_xys_info(runtime_of_dirts_dict[key2])
	plot_simple_graph(key1, 'Dirt Piles Num', 'Runtime / Dirt Piles Num', True, plt.plot, k1_x, k1_y)
	plot_simple_graph(key2, 'Dirt Piles Num', 'Runtime / Dirt Piles Num', True, plt.plot, k2_x, k2_y)
	print 'wilcoxon:', wilcoxon(k1_y, k2_y)
	print key1, 'rank:', k1_rank
	print key2, 'rank:', k2_rank

def get_dict_info(list):
	d = { 1:[], 2:[], 3:[] }
	for x, y in list:
		d[x] = y
	for x in d:
		d[x] = average(d[x])
	return [d[1], d[2], d[3]], 1*d[1]+2*d[2]+1*d[3]
	
len_of_robots_test = {'DirtsDivisionHeuristic': [(1, 98), (1, 96), (1, 109), (1, 100), (1, 98), (1, 113), (1, 98), (1, 112), (1, 107), (1, 102), (1, 91), (1, 90), (1, 90), (1, 94), (1, 107), (1, 90), (1, 83), (1, 98), (1, 114), (2, 54), (2, 58), (2, 56), (2, 72), (2, 66), (2, 71), (2, 59), (2, 51), (2, 78), (2, 54), (2, 52), (2, 52), (2, 71), (2, 68), (2, 65), (2, 51), (2, 70), (2, 64), (2, 54), (3, 41), (3, 50), (3, 54), (3, 51), (3, 39), (3, 33), (3, 48), (3, 50), (3, 51), (3, 49), (3, 56), (3, 44), (3, 46), (3, 49), (3, 37), (3, 59), (3, 59), (3, 62), (3, 55)], 'OneDirtPerRobotHeuristic': [(1, 108), (1, 102), (1, 117), (1, 97), (1, 113), (1, 125), (1, 94), (1, 112), (1, 94), (1, 100), (1, 97), (1, 84), (1, 90), (1, 94), (1, 111), (1, 86), (1, 95), (1, 98), (1, 108), (2, 50), (2, 68), (2, 43), (2, 50), (2, 60), (2, 41), (2, 46), (2, 43), (2, 47), (2, 59), (2, 56), (2, 68), (2, 45), (2, 61), (2, 66), (2, 47), (2, 67), (2, 59), (2, 50), (3, 35), (3, 37), (3, 30), (3, 40), (3, 38), (3, 31), (3, 33), (3, 27), (3, 29), (3, 32), (3, 43), (3, 33), (3, 33), (3, 38), (3, 34), (3, 42), (3, 35), (3, 31), (3, 46)], 'AStarAnyTime': [(1, 108), (1, 102), (1, 117), (1, 97), (1, 113), (1, 125), (1, 94), (1, 112), (1, 94), (1, 100), (1, 97), (1, 84), (1, 90), (1, 94), (1, 111), (1, 86), (1, 95), (1, 98), (1, 108), (2, 50), (2, 68), (2, 43), (2, 50), (2, 60), (2, 41), (2, 46), (2, 43), (2, 47), (2, 59), (2, 56), (2, 68), (2, 45), (2, 61), (2, 66), (2, 47), (2, 67), (2, 59), (2, 50), (3, 35), (3, 37), (3, 30), (3, 40), (3, 38), (3, 31), (3, 33), (3, 27), (3, 29), (3, 32), (3, 43), (3, 33), (3, 33), (3, 38), (3, 34), (3, 42), (3, 35), (3, 31), (3, 46)], 'BeamSearchAnyTime': [(1, 104), (1, 100), (1, 109), (1, 101), (1, 104), (1, 125), (1, 98), (1, 146), (1, 103), (1, 85), (1, 100), (1, 91), (1, 92), (1, 96), (1, 103), (1, 101), (1, 92), (1, 94), (1, 112), (2, 51), (2, 67), (2, 43), (2, 50), (2, 61), (2, 41), (2, 45), (2, 42), (2, 49), (2, 47), (2, 57), (2, 67), (2, 42), (2, 57), (2, 66), (2, 47), (2, 48), (2, 62), (2, 51), (3, 36), (3, 37), (3, 30), (3, 40), (3, 37), (3, 28), (3, 33), (3, 27), (3, 31), (3, 36), (3, 43), (3, 36), (3, 33), (3, 39), (3, 34), (3, 43), (3, 40), (3, 33), (3, 44)]}
def process_len_of_robots(key1, key2):
	print '### comparing solution quality between', key1, 'and', key2, '###'
	k1_avgs, k1_rank = get_dict_info(len_of_robots_test[key1])
	k2_avgs, k2_rank = get_dict_info(len_of_robots_test[key2])
	width = 0.5
	plot_simple_graph(key1, 'Robots Num', 'Average Solution Quality (Length)', False, plt.bar, [x-width/2 for x in [1, 2, 3]], k1_avgs, width)
	plot_simple_graph(key2, 'Robots Num', 'Average Solution Quality (Length)', False, plt.bar, [x-width/2 for x in [1, 2, 3]], k2_avgs, width)
	print 'wilcoxon:', wilcoxon(k1_avgs, k2_avgs)
	print key1, 'rank:', k1_rank
	print key2, 'rank:', k2_rank

agent_test = [(10, 78.0), (25, 58.0), (40, 74.0), (55, 77.0), (70, 67.0), (85, 53.0), (100, 56.0), (115, 66.0), (130, 71.0), (145, 64.0), (160, 62.0), (175, 56.0), (190, 55.0), (205, 53.0), (220, 57.0), (235, 73.0), (250, 60.0), (265, 63.0), (280, 62.0), (295, 49.0)]
def process_len_of_limit():
	print '### processing solution quality ###'
	xs, ys, rank = get_xys_info(agent_test)
	plot_simple_graph('RobotsAgent', 'Time Limit', 'Solution Quality (Length)', True, plt.plot, xs, ys)
	
if __name__ == '__main__':
	#process_runtime_of_dirt('DirtsDivisionHeuristic', 'OneDirtPerRobotHeuristic')
	#process_runtime_of_dirt('AStar', 'BeamSearch')
	process_len_of_robots('DirtsDivisionHeuristic', 'OneDirtPerRobotHeuristic')
	process_len_of_robots('AStarAnyTime', 'BeamSearchAnyTime')
	#process_len_of_limit()
	plt.show()