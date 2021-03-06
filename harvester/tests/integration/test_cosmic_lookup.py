
import json
import sys
import time
import logging
sys.path.append('.')  # NOQA
import jax
import cosmic_lookup_table

LOOKUP_TABLE = cosmic_lookup_table.CosmicLookup("./cosmic_lookup_table.tsv")

JAX_FEATURES = [
    'BRAF V600E ',
    'EML4-ALK',
    'KRAS  mutant',
    'NPM1-ALK',
    'EGFR T790M ',
    'EGFR L858R ',
    'PTEN  loss',
    'PIK3CA H1047R ',
    'ERBB2  amp',
    'FLT3  ',
    'KRAS G12D ',
    'MET  amp',
    'ERBB2  positive',
    'PIK3CA  mutant',
    'PIK3CA E545K ',
    'FGFR1  amp',
    'KRAS G13D ',
    'BRAF  mut',
    'EGFR  amp',
    'EGFR E746_A750del ',
    'FGFR2  amp',
    'NRAS  mutant',
    'EGFR  ',
    'BRAF  mutant',
    'ERBB2  over exp',
    'KRAS  wild-type',
    'KIT W557_K558del ',
    'KRAS G12V ',
    'MET  over exp',
    'NRAS Q61K ',
    'KRAS  mut',
    'PTEN  inact mut',
    'ALK L1198F ',
    'KRAS G12C ',
    'APC  inact mut',
    'JAK2 V617F ',
    'PIK3CA  act mut',
    'PIK3CA  mut',
    'ALK L1196M ',
    'EGFR C797S ',
    'FGFR3-TACC3',
    'PIK3CA  wild-type',
    'BRAF V600X ',
    'EGFR  act mut',
    'BRAF  wild-type',
    'MET  ',
    'ALK G1269A ',
    'ERBB2  pos',
    'TP53  wild-type',
    'ALK D1203N ',
    'RB1  wild-type',
    'ALK  rearrange',
    'ALK C1156Y ',
    'FLT3 F691L ',
    'KIT  ',
    'AKT1 E17K ',
    'KRAS G12S ',
    'PIK3CA E542K ',
    'EZH2  pos',
    'ALK  fusion',
    'BRCA1  mutant',
    'EGFR  wild-type',
    'ERBB2 L755S ',
    'NRAS A146T ',
    'PTEN  mutant',
    'ALK F1174L ',
    'ALK G1202R ',
    'EGFR  mutant',
    'FGFR3  over exp',
    'RET M918T ',
    'IDH1 R132H ',
    'ALK I1171T ',
    'CDKN2A  loss',
    'EGFR  over exp',
    'EGFR G719A ',
    'FGFR1  positive',
    'ALK E1210K ',
    'BRCA2  mutant',
    'EGFR  positive',
    'ERBB2  ',
    'KIT D816V ',
    'MAP2K1 L115P ',
    'MAP2K1 P387S ',
    'PTEN  del',
    'EGFR G465R ',
    'FGFR2 N549K ',
    'FGFR3 S249C ',
    'KIT T670I ',
    'MAP2K1 Q56P ',
    'NRAS  wild-type',
    'PTEN  wild-type',
    'ALK F1174C ',
    'ALK I1171S ',
    'BRAF V600K ',
    'EGFR L718Q ',
    'EGFR L844V ',
    'ERBB2 S310F ',
    'MET  positive',
    'RB1  loss',
    'ALK C1156F ',
    'ALK F1174V ',
    'ALK I1171N ',
    'ALK R1192P ',
    'BRAF V600E/K ',
    'ERBB2 T798M ',
    'FGFR3 K650E ',
    'HRAS G12V ',
    'IDH1  mutant',
    'KRAS A146T ',
    'KRAS G12R ',
    'PTEN  mut',
    'ALK T1151M ',
    'BRAF G466V ',
    'FGFR2 S252W ',
    'FLT3 D835Y ',
    'KRAS G12X ',
    'KRAS Q61H ',
    'MET Y1230H ',
    'ALK  wild-type',
    'ERBB2 V777L ',
    'ETV6-NTRK3',
    'KIT V560D ',
    'MET D1228N ',
    'NOTCH1  wild-type',
    'NRAS G12D ',
    'PIK3CA  amp',
    'RET C634W ',
    'EGFR L861Q ',
    'ERBB2 G778_P780dup ',
    'EZH2 Y641N ',
    'GNAQ Q209L ',
    'HRAS Q61L ',
    'KIT A829P ',
    'KIT V654A ',
    'PTEN  dec exp',
    'RET C634R ',
    'ALK  positive',
    'BRCA1  wild-type',
    'EGFR E709_T710delinsD ',
    'ERBB2  mutant',
    'ERBB2 L866M ',
    'ERBB2 V842I ',
    'ETV6-JAK2',
    'FGFR2 N550K ',
    'FLT3  act mut',
    'MAP2K1 C121S ',
    'MAP2K1 V211D ',
    'NPM1  mutant',
    'PIK3CA Q546K ',
    'TP53  mutant',
    'ALK L1122V ',
    'ATM  inact mut',
    'BRAF V600D ',
    'EGFR  pos',
    'EZH2 Y111D ',
    'FBXW7  inact mut',
    'FGFR1  over exp',
    'FGFR2  act mut',
    'FGFR2  wild-type',
    'HRAS  mutant',
    'IDH1 R132C ',
    'JAK2  over exp',
    'KIT N822K ',
    'KMT2A  rearrange',
    'MET  act mut',
    'MET Y1230C ',
    'NOTCH1  mut',
    'PDGFRA D842V ',
    'PIK3CA G1049R ',
    'RET  rearrange',
    'ALK V1180L ',
    'EGFR G719S ',
    'FGFR1  act mut',
    'FGFR2  fusion',
    'FGFR3  act mut',
    'FGFR3 N540K ',
    'FGFR3 Y373C ',
    'FGFR3-BAIAP2L1',
    'FLT3  mutant',
    'KIT V560G ',
    'KRAS  amp',
    'MET  pos',
    'MET  wild-type',
    'MPL W515L ',
    'NOTCH1  positive',
    'PIK3CA D549N ',
    'PIK3CA N345K ',
    'PIK3CA P449T ',
    'SRC  positive',
    'ALK F1174I ',
    'ALK F1245C ',
    'ALK G1128S ',
    'ALK N1178H ',
    'BRAF  act mut',
    'BRAF G469A ',
    'BRCA2  inact mut',
    'BRCA2  loss',
    'BRCA2  wild-type',
    'EGFR E709K ',
    'EGFR S492R ',
    'EGFR S768I ',
    'ERBB2 L869R ',
    'ERBB2 Y772_A775dup ',
    'EZH2 Y641S ',
    'FGFR2  over exp',
    'FGFR3  mutant',
    'FGFR3  wild-type',
    'FGFR3 L608V ',
    'FGFR3 V555M ',
    'FLT3 Y599_D600insSTDNEYFYVDFREYEY ',
    'FLT3 Y842C ',
    'HRAS G13R ',
    'JAK2 G935R ',
    'KIT D820Y ',
    'KIT L576P ',
    'KIT V559D ',
    'KIT V560_Y578del ',
    'KRAS  ',
    'KRAS A146V ',
    'MAP2K1 K57N ',
    'MAP2K1 K59del ',
    'MET  dec exp',
    'NRAS Q61L ',
    'PDGFRA  amp',
    'PIK3CA H1047L ',
    'PIK3CA K111N ',
    'PIK3CA P539R ',
    'ROS1  rearrange',
    'RUNX1-RUNX1T1',
    'SMARCB1  negative',
    'STK11  inact mut',
    'TP53  mut',
    'ALK S1206C ',
    'ATM  loss',
    'BRAF  amp',
    'BRAF D594G ',
    'BRAF G466E ',
    'BRAF K601E ',
    'BRAF L597V ',
    'BRAF V600R ',
    'BRCA1  inact mut',
    'EGFR  dec exp',
    'EGFR  mut',
    'EGFR D770delinsGY ',
    'EGFR G719X ',
    'ERBB2 C805S ',
    'ERBB2 S310Y ',
    'FGFR2 K310R ',
    'FGFR2 V564F ',
    'FGFR3  amp',
    'FGFR3 Y375C ',
    'FLT3  wild-type',
    'JAK3 L857P ',
    'KIT D816H ',
    'KIT D820A ',
    'KIT D820G ',
    'KMT2A-AFF1',
    'KRAS G12A ',
    'KRAS G13X ',
    'KRAS Q61K ',
    'MAP2K1 P124L ',
    'MET D1228V ',
    'MYD88 L265P ',
    'NRAS  mut',
    'NRAS Q61R ',
    'PIK3CA G118D ',
    'PIK3CA H1047X ',
    'PIK3CA R88Q ',
    'SRC T341M ',
    'TP53 R175H ',
    'ALK G1202del ',
    'ALK L1152R ',
    'ALK P1139S ',
    'ALK R1275Q ',
    'ALK S1206Y ',
    'BRAF G464V ',
    'BRAF T529I ',
    'BRAF T529M ',
    'BRAF T529N ',
    'EGFR A763_Y764insFQEA ',
    'EGFR L698_S1037dup ',
    'EGFR N771_H773dup ',
    'ERBB2  act mut',
    'ERBB2 M774delinsWLV ',
    'FLT3 F691I ',
    'FLT3 Y842H ',
    'HRAS G12R ',
    'IDH2  mutant',
    'IDH2 R172K ',
    'JAK2 E864K ',
    'JAK2 I960V ',
    'JAK2 R683G ',
    'JAK2 R867Q ',
    'JAK2 R938L ',
    'KIT  mutant',
    'KIT K642E ',
    'KMT2A-MLLT3',
    'KRAS  act mut',
    'KRAS G13R ',
    'MAP2K1 I103N ',
    'MAP2K1 V60E ',
    'NPM1-ALK  amp',
    'PIK3CA  over exp',
    'RB1  inact mut',
    'RET  mutant',
    'RET C634Y ',
    'RET V804M ',
    'SMO D384N ',
    'SMO D473G ',
    'SMO E518K ',
    'SMO S387N ',
    'SRC  act mut',
    'STAG2  dec exp',
    'TP53  loss',
    'ABL1 R332W ',
    'AKT1  act mut',
    'AKT1  mutant',
    'ALK  amp',
    'ALK D1091N ',
    'APC  mutant',
    'APC  wild-type',
    'APC E853* ',
    'ATRX  loss',
    'BRAF D594N ',
    'BRAF G596R ',
    'BRAF N486_P490del ',
    'BRAF V487_P492delinsA ',
    'BRCA1  dec exp',
    'BRCA2  del',
    'CDKN2A  del',
    'EGFR D761Y ',
    'EGFR G465E ',
    'EGFR G719C ',
    'EGFR K467T ',
    'EGFR L792F ',
    'EGFR Q791R ',
    'EGFR R451C ',
    'EGFR S464L ',
    'EGFR S768_D770dup ',
    'EGFR T34_A289del ',
    'EGFR V769_D770insASV ',
    'EGFR-RAD51',
    'ERBB2 G776delinsVC ',
    'ERBB2 L755P ',
    'EZH2 A677G ',
    'FGFR1  dec exp',
    'FGFR2  mutant',
    'FGFR2  positive',
    'FGFR2 K660E ',
    'FGFR3  dec exp',
    'FGFR3  positive',
    'FLT3 D835G ',
    'FLT3 D835H ',
    'FLT3 D835V ',
    'FLT3 R834Q ',
    'GNAQ Q209P ',
    'IDH1 R132X ',
    'KDR  act mut',
    'KIT  act mut',
    'KIT D816G ',
    'KIT K550_W557del ',
    'KIT K558delinsNP ',
    'KIT V560del ',
    'KIT Y823D ',
    'KMT2A-MLLT1',
    'KRAS G13C ',
    'MAP2K1 G128V ',
    'MAP2K1 K57T ',
    'MAP2K1 P124Q ',
    'MAP2K1 P124S ',
    'MPL  over exp',
    'MPL  wild-type',
    'NOTCH1  act mut',
    'NRAS G12V ',
    'NRAS G13D ',
    'PIK3CA C420R ',
    'PTEN  pos',
    'PTEN R130G ',
    'PTEN R130Q ',
    'PTPN11 E76K ',
    'RB1  mut',
    'ROS1  fusion',
    'SMO  amp',
    'SMO A459V ',
    'SMO C469Y ',
    'SMO D473H ',
    'SMO I408V ',
    'SMO N219D ',
    'SMO T241M ',
    'SMO V321M ',
    'SMO W281C ',
    'SMO W535L ',
    'STK11  loss',
    'TP53 R248W ',
    'AKT1  wild-type',
    'AKT1 Q79K ',
    'ALK L1152P ',
    'ALK T1151dup ',
    'APC L665* ',
    'APC N1819fs ',
    'APC Q1338* ',
    'APC R1450* ',
    'APC S1197* ',
    'APC S1278* ',
    'APC S811* ',
    'APC T1556fs ',
    'ATM  dec exp',
    'ATM  over exp',
    'BRAF  ',
    'BRAF G466A ',
    'BRAF G469R ',
    'BRAF L485_P490delinsY ',
    'BRAF L597S ',
    'BRCA1  loss',
    'BRCA1  mut',
    'BRCA1 E23Vfs*17 ',
    'BRCA2  dec exp',
    'CDH1  over exp',
    'CDKN2A  mut',
    'CSF1R  positive',
    'CTNNB1  mutant',
    'EGFR D770_N771insSVD ',
    'EGFR E884K ',
    'EGFR H773_V774insH ',
    'EGFR H773_V774insNPH ',
    'EGFR I491M ',
    'EGFR L747_S752del ',
    'EGFR L747_T751delinsP ',
    'EGFR N826S ',
    'ERBB2 D277H ',
    'ERBB2 D769H ',
    'ERBB2 D769Y ',
    'ERBB2 G309A ',
    'ERBB2 K753E ',
    'ERBB2 L726F ',
    'ERBB2 L755_T759del ',
    'ERBB2 L768S ',
    'ERBB2 R896C ',
    'ERBB2 S653C ',
    'ERBB2 T798I ',
    'ERBB2 V659E ',
    'ERBB2 V773L ',
    'ERBB4 G1109C ',
    'EZH2  positive',
    'EZH2 F120L ',
    'EZH2 Y111N ',
    'FBXW7 R505C ',
    'FGFR1  rearrange',
    'FGFR1  wild-type',
    'FGFR1-TACC1',
    'FGFR2  pos',
    'FGFR2 E566G ',
    'FGFR2 I548V ',
    'FGFR2 L618M ',
    'FGFR2 M536I ',
    'FGFR2 M538I ',
    'FGFR2 N550H ',
    'FGFR2 N550S ',
    'FGFR2 V565I ',
    'FGFR2-BICC1',
    'FGFR3  fusion',
    'FGFR3 G384D ',
    'FLT3 A848P ',
    'FLT3 N676D ',
    'GNA11  mutant',
    'GNA11 Q209L ',
    'GNAQ  mutant',
    'IDH1 R132S ',
    'IDH2 R140Q ',
    'JAK3 V674A ',
    'JAK3 Y100A ',
    'KDR  positive',
    'KDR  wild-type',
    'KIT  positive',
    'KIT S476I ',
    'KIT V560_L576del ',
    'KRAS Q61X ',
    'MAP2K1 E203K ',
    'MAP2K1 F53L ',
    'MET  amp over exp',
    'MET F1200L ',
    'MET G1163R ',
    'MET N375S ',
    'NOTCH1  rearrange',
    'NPM1  ',
    'NRAS  amp',
    'PDGFRA V561D ',
    'PIK3CA H1047Y ',
    'PIK3CA I20M ',
    'PTEN  negative',
    'PTEN T321fs*23 ',
    'RB1  positive',
    'RET S891A ',
    'RET V804L ',
    'SMAD4  del',
    'TP53  del',
    'TP53 R273* ',
    'TP53 R282W ',
    'ABL1 G321L ',
    'ABL1 T315I ',
    'AKT1  over exp',
    'AKT1  positive',
    'ALK L1196Q ',
    'APC I1164fs ',
    'APC R216* ',
    'APC W553* ',
    'ASXL1  wild-type',
    'ATM  del',
    'BRAF F247L ',
    'BRAF G469V ',
    'BRAF K601N ',
    'BRAF L505H ',
    'BRAF L597R ',
    'BRAF N581S ',
    'CALR  mutant',
    'CBL  mutant',
    'CBLC  dec exp',
    'CEBPA  mutant',
    'DNMT3A  mut',
    'EGFR A289T ',
    'EGFR E709X ',
    'EGFR I744_K745insKIPVAI ',
    'EGFR L747S ',
    'EGFR L747_P753delinsS ',
    'EGFR P772_H773insPNP ',
    'EGFR-SEPT14',
    'ERBB2  dec exp',
    'ERBB2  wild-type',
    'ERBB2 E717K ',
    'ERBB2 E719G ',
    'ERBB2 E812K ',
    'ERBB2 G660D ',
    'ERBB2 G776delinsLC ',
    'ERBB2 H878Y ',
    'ERBB2 L785F ',
    'ERBB2 N857S ',
    'ERBB2 P780L ',
    'ERBB2 R678Q ',
    'ERBB2 S783P ',
    'ERBB2 T733I ',
    'ERBB2 T862A ',
    'ERBB2 V773A ',
    'ERBB2 Y803N ',
    'ETV6-RUNX1',
    'EZH2 Y641F ',
    'EZH2 Y646F ',
    'EZH2 Y646N ',
    'FBXW7 R465H ',
    'FGFR1  fusion',
    'FGFR1  pos',
    'FGFR1 T141R ',
    'FGFR2  dec exp',
    'FGFR2 S267_D273dup ',
    'FGFR2 W290_I291delinsC ',
    'FGFR2-AHCYL1',
    'FGFR2-TACC3',
    'FGFR3  rearrange',
    'FLT3 D698N ',
    'FLT3 D835E ',
    'FLT3 D835F ',
    'FLT3 D835N ',
    'FLT3 D835X ',
    'FLT3 D839A ',
    'FLT3 D839G ',
    'FLT3 D839H ',
    'FLT3 D839N ',
    'FLT3 G846R ',
    'FLT3 I836del ',
    'FLT3 M664I ',
    'FLT3 N676S ',
    'FLT3 N841K ',
    'FLT3 R845G ',
    'FLT3 Y842S ',
    'GATA1  over exp',
    'GATA2  mutant',
    'HRAS  wild-type',
    'HRAS K117E ',
    'HRAS Q61R ',
    'JAK2  amp',
    'JAK2 M929I ',
    'JAK2 Y931C ',
    'JAK3 A572V ',
    'KDR Q472H ',
    'KIT  over exp',
    'KIT  wild-type',
    'KIT A502_Y503dup ',
    'KIT D816Y ',
    'KIT D820E ',
    'KIT H697Y ',
    'KIT K558_G565delinsR ',
    'KIT N505I ',
    'KIT N822I ',
    'KIT P577del ',
    'KIT V559A ',
    'KIT W557C ',
    'KIT W557Lfs*5 ',
    'KIT W557R ',
    'KIT Y578C ',
    'KMT2A  fusion',
    'KMT2A-MLLT10',
    'KRAS A146P ',
    'KRAS A59G ',
    'KRAS K117N ',
    'MAP2K1 I111N ',
    'MAP2K1 K57E ',
    'MAP2K1 Y134C ',
    'MET M1268T ',
    'MET R988C ',
    'MET Y1230S ',
    'MSH6  loss',
    'MSH6  mutant',
    'NOTCH1 A1707T ',
    'NRAS  over exp',
    'NRAS G12X ',
    'NRAS G13X ',
    'NRAS Q61X ',
    'PDGFRA D842Y ',
    'PDGFRA G853D ',
    'PDGFRA H845Y ',
    'PDGFRA N659K ',
    'PDGFRA P577S ',
    'PDGFRA R841K ',
    'PDGFRA V658A ',
    'PDGFRA Y849S ',
    'PIK3CA E365K ',
    'PIK3CA I391M ',
    'PIK3CA Q546R ',
    'PIK3CA R38C ',
    'PTEN  positive',
    'PTEN A126G ',
    'PTEN A72fs*5 ',
    'PTEN I253N ',
    'PTEN L108R ',
    'PTEN N69D ',
    'PTEN R308C ',
    'RET  fusion',
    'RET  positive',
    'RET  wild-type',
    'RET A883F ',
    'RET E768D ',
    'RET L790F ',
    'RET Y791F ',
    'RET Y806C ',
    'RUNX1  mutant',
    'SF3B1 K700E ',
    'SMAD4  dec exp',
    'SMAD4  mut',
    'SMAD4 Q83* ',
    'SMO  wild-type',
    'SMO Q477E ',
    'SRC  over exp',
    'TET2  mutant',
    'TP53 H168R ',
    'ABL1 G250R ',
    'ABL1 G251D ',
    'AKT1  amp',
    'AKT1 W80A ',
    'ALK  ',
    'ALK  act mut',
    'ALK  mut',
    'ALK  mutant',
    'ALK F1245V ',
    'ALK G1128A ',
    'ALK S1206F ',
    'ALK Y1278S ',
    'APC  mut',
    'APC E1309* ',
    'APC G1416* ',
    'APC K1555* ',
    'APC L1488* ',
    'APC Q1131* ',
    'APC Q1303* ',
    'APC Q1429fs ',
    'ASXL1  inact mut',
    'ASXL1  mutant',
    'ATM  mut',
    'ATM  mutant',
    'ATM L804fs*4 ',
    'ATM S978fs*12 ',
    'ATRX  inact mut',
    'BCOR  mutant',
    'BCOR-RARA',
    'BCORL1  over exp',
    'BRAF  dec exp',
    'BRAF F595L ',
    'BRAF G464E ',
    'BRAF G464R ',
    'BRAF G469L ',
    'BRAF G596V ',
    'BRAF K601T ',
    'BRAF L485Y ',
    'BRAF L597Q ',
    'BRAF N581Y ',
    'BRAF Y472C ',
    'BRCA1  negative',
    'BRCA1 C61G ',
    'BRCA1 L1795Pfs*3 ',
    'BRCA1 L392Qfs*5 ',
    'BRCA1 L631Qfs*4 ',
    'BRCA1 N682* ',
    'BRCA1 W1782* ',
    'BRCA2  mut',
    'BRCA2  negative',
    'BRCA2 N136Ifs*16 ',
    'BRCA2 N136_L139del ',
    'BRCA2 V130_N136delinsD ',
    'CBL  dec exp',
    'CBL  del',
    'CBLB  dec exp',
    'CBLB  del',
    'CBLC  over exp',
    'CDH1  mutant',
    'CDH1 R63* ',
    'CDKN2A  mutant',
    'CDKN2A  over exp',
    'CDKN2A  pos',
    'CDKN2A R80* ',
    'CEBPA  positive',
    'CSF1R  over exp',
    'CSF1R Y571D ',
    'CSF3R  mutant',
    'CSF3R T618I ',
    'CSF3R T640N ',
    'CTNNB1  act mut',
    'CTNNB1  amp',
    'CTNNB1  mut',
    'CTNNB1  over exp',
    'CTNNB1  wild-type',
    'CTNNB1 S45F ',
    'CTNNB1 T41A ',
    'DNMT3A R882H ',
    'EGFR A289V ',
    'EGFR A702S ',
    'EGFR A750P ',
    'EGFR A750V ',
    'EGFR A767_V769dup ',
    'EGFR D770_N771insNPG ',
    'EGFR E734Q ',
    'EGFR E868G ',
    'EGFR H835L ',
    'EGFR I941R ',
    'EGFR K745_E746insIPVAIK ',
    'EGFR K745_E746insTPVAIK ',
    'EGFR L747_E749del ',
    'EGFR L747_T751del ',
    'EGFR L833F ',
    'EGFR L833V ',
    'EGFR L858M ',
    'EGFR R108K ',
    'EGFR R521K ',
    'EGFR R776H ',
    'EGFR R831H ',
    'EGFR S752I ',
    'EGFR T263P ',
    'EGFR T854A ',
    'EGFR V769L ',
    'EGFR V769M ',
    'EGFR Y764_V765insHH ',
    'EGFR-PURB',
    'ERBB2 A775_G776insYVMA ',
    'ERBB2 D821N ',
    'ERBB2 G776V ',
    'ERBB2 G776_V777insYVMA ',
    'ERBB2 G778_S779insCPG ',
    'ERBB2 L726I ',
    'ERBB2 L869Q ',
    'ERBB2 L915M ',
    'ERBB2 V839G ',
    'ERBB4 E317K ',
    'ERBB4 E452K ',
    'ERBB4 E563K ',
    'ERBB4 R393W ',
    'ERBB4 R544W ',
    'ETV6  inact mut',
    'ETV6  mutant',
    'ETV6-ALK',
    'ETV6-FGFR1',
    'ETV6-FGFR3',
    'ETV6-FGFR4',
    'ETV6-NTRK2',
    'ETV6-PDGFRA',
    'ETV6-ROS1',
    'ETV6-SYK',
    'EZH2  mutant',
    'EZH2  over exp',
    'EZH2  wild-type',
    'EZH2 T678_R679delinsKK ',
    'EZH2 Y641C ',
    'EZH2 Y641H ',
    'EZH2 Y646H ',
    'EZH2 Y646S ',
    'FBXW7  del',
    'FBXW7  loss',
    'FBXW7 R465C ',
    'FBXW7 R479Q ',
    'FBXW7 R505L ',
    'FGFR1  mutant',
    'FGFR1 V561M ',
    'FGFR2 C383R ',
    'FGFR2 E565A ',
    'FGFR2 K659M ',
    'FGFR2 K660N ',
    'FGFR2 M186T ',
    'FGFR2 N549H ',
    'FGFR2 V564I ',
    'FGFR2 V564L ',
    'FGFR2-CCDC6',
    'FGFR2-FAM76A',
    'FGFR2-ZMYM4',
    'FGFR3  mut',
    'FGFR3  pos',
    'FGFR3 D764N ',
    'FGFR3 D788N ',
    'FGFR3 F386L ',
    'FGFR3 G372C ',
    'FGFR3 K650M ',
    'FGFR3 K652E ',
    'FGFR3 R248C ',
    'FGFR3 S131L ',
    'FGFR3 V555L ',
    'FLT3  amp',
    'FLT3 E598_Y599insGLVQVTGSSDNEYFYVDFREYE ',
    'FLT3 E612_F613insGYVDFREYEYDLKWEFRPRENLEF ',
    'FLT3 L601_K602insREYEYDL ',
    'FLT3 L611_E612insCSSDNEYFYVDFREYEYDLKWEFPRENL ',
    'FLT3 M837G ',
    'FLT3 S451F ',
    'FLT3 S652G ',
    'FLT3 S838R ',
    'FLT3 V592G ',
    'FLT3 Y572C ',
    'FLT3 Y599_D600insGLYVDFREYEY ',
    'FOXL2 C134W ',
    'GATA1  mutant',
    'GATA2  wild-type',
    'HNF1A  inact mut',
    'HRAS  inact mut',
    'HRAS Q61K ',
    'IDH1 R132G ',
    'IDH1 R132L ',
    'IDH2 D76fs ',
    'IDH2 R140W ',
    'IKZF1  del',
    'IKZF1  wild-type',
    'JAK2  inact mut',
    'JAK2 E985K ',
    'JAK2 G831R ',
    'JAK2 N909K ',
    'JAK2 P1057S ',
    'JAK2 R1127K ',
    'JAK2 R975G ',
    'JAK2 V881A ',
    'JAK2 Y918H ',
    'JAK3 E183G ',
    'JAK3 I87T ',
    'JAK3 L156P ',
    'JAK3 R172Q ',
    'JAK3 V722I ',
    'KDM6A  loss',
    'KDR  amp',
    'KDR  over exp',
    'KDR  pos',
    'KDR A1065T ',
    'KDR D717V ',
    'KDR R961W ',
    'KDR V297I ',
    'KIT  amp',
    'KIT  mut',
    'KIT C443S ',
    'KIT D579del ',
    'KIT D816E ',
    'KIT D820V ',
    'KIT K558_V560del ',
    'KIT M541L ',
    'KIT M552_K558del ',
    'KIT M552_V559del ',
    'KIT P551_V555del ',
    'KIT P551_V555delinsTL ',
    'KIT P551_W557delinsL ',
    'KIT P577_D579del ',
    'KIT T417_D419delinsI ',
    'KIT V559del ',
    'KIT W557G ',
    'KIT W557_V559delinsF ',
    'KIT Y553N ',
    'KMT2A-ELL',
    'KMT2A-EP300',
    'KMT2A-GAS7',
    'KMT2A-SEPT6',
    'KRAS A59T ',
    'KRAS G12F ',
    'KRAS Q61L ',
    'MAP2K1  mutant',
    'MAP2K1 D351G ',
    'MAP2K1 F129L ',
    'MAP2K1 F53S ',
    'MAP2K1 H119P ',
    'MAP2K1 H119Y ',
    'MAP2K1 L115A ',
    'MET  negative',
    'MET D1228H ',
    'MET E168D ',
    'MET H1112L ',
    'MET H1112Y ',
    'MET L1195V ',
    'MET L1213V ',
    'MET M1250T ',
    'MET T1010I ',
    'MET V1110I ',
    'MET V1206L ',
    'MET V1238I ',
    'MET Y1230D ',
    'MET Y1248H ',
    'MLH1  inact mut',
    'MLH1  loss',
    'MLH1  mutant',
    'MPL W515K ',
    'MSH6 T1219I ',
    'MYD88  act mut',
    'MYD88  mutant',
    'MYD88  wild-type',
    'NOTCH1  mutant',
    'NOTCH1  over exp',
    'NOTCH1 A1552G ',
    'NOTCH1 A1552V ',
    'NOTCH1 A1570G ',
    'NOTCH1 C478F ',
    'NOTCH1 E1567K ',
    'NOTCH1 I1680S ',
    'NOTCH1 R1683W ',
    'NOTCH1 S2449fs ',
    'NOTCH1 V1575A ',
    'NOTCH1 V1599M ',
    'NOTCH1 V1676I ',
    'NPM1 W288fs ',
    'NRAS G13R ',
    'NRAS G13V ',
    'NRAS T58I ',
    'PDGFRA  act mut',
    'PDGFRA  mut',
    'PDGFRA  mutant',
    'PDGFRA  rearrange',
    'PDGFRA D842X ',
    'PDGFRA D842_I843delinsIM ',
    'PDGFRA D846Y ',
    'PDGFRA H650Q ',
    'PDGFRA H845_N848delinsP ',
    'PDGFRA I843del ',
    'PDGFRA L221F ',
    'PDGFRA N659S ',
    'PDGFRA R748G ',
    'PDGFRA R841_D842delinsKI ',
    'PDGFRA S566_E571delinsR ',
    'PDGFRA V561_I562insER ',
    'PIK3CA D1029Y ',
    'PIK3CA D350G ',
    'PIK3CA D939G ',
    'PIK3CA E453K ',
    'PIK3CA E453del ',
    'PIK3CA E542V ',
    'PIK3CA E545V ',
    'PIK3CA E545X ',
    'PIK3CA E545k ',
    'PIK3CA E726K ',
    'PIK3CA E78K ',
    'PIK3CA F930S ',
    'PIK3CA G106_R108del ',
    'PIK3CA H1047K ',
    'PIK3CA K111R ',
    'PIK3CA K567R ',
    'PIK3CA K944N ',
    'PIK3CA K966E ',
    'PIK3CA M1043V ',
    'PIK3CA Q546L ',
    'PIK3CA R108H ',
    'PIK3CA R425L ',
    'PIK3CA R88L ',
    'PIK3CA R93W ',
    'PIK3CA T1025A ',
    'PIK3CA T1025K ',
    'PIK3CA V344G ',
    'PIK3CA V952A ',
    'PIK3CA V955G ',
    'PIK3CA V955I ',
    'PTEN  ',
    'PTEN C136Y ',
    'PTEN E307K ',
    'PTEN G129R ',
    'PTEN G143fs*4 ',
    'PTEN H93D ',
    'PTEN K267fs*9 ',
    'PTEN K6fs*4 ',
    'PTEN R130* ',
    'PTEN R173S ',
    'PTEN R55fs*1 ',
    'PTEN T319fs*1 ',
    'PTEN V275* ',
    'PTEN V54fs ',
    'PTEN Y27fs*1 ',
    'PTEN Y86fs ',
    'PTPN11  act mut',
    'PTPN11  dec exp',
    'PTPN11  mutant',
    'RAD21  wild-type',
    'RB1  mutant',
    'RB1 C706F ',
    'RET  act mut',
    'RET  over exp',
    'RET C618R ',
    'RET C620R ',
    'RET C634F ',
    'RET D898V ',
    'RET E884K ',
    'RET G691S ',
    'RET M1009T ',
    'RET V804G ',
    'RET Y806E ',
    'RET Y806F ',
    'ROS1  pos',
    'ROS1  positive',
    'SETBP1  mutant',
    'SF3B1  mutant',
    'SF3B1 K666N ',
    'SMAD4  inact mut',
    'SMAD4  loss',
    'SMAD4 Q249H ',
    'SMARCB1  del',
    'SMARCB1  inact mut',
    'SMARCB1  loss',
    'SMO  dec exp',
    'SMO D384A ',
    'SMO F460L ',
    'SMO H231R ',
    'SMO L325F ',
    'SMO L412F ',
    'SMO M525G ',
    'SMO R400A ',
    'SMO S533N ',
    'SMO T466F ',
    'SMO V329F ',
    'SMO Y394A ',
    'SRC  amp',
    'SRC  pos',
    'SRC T341I ',
    'STK11  mut',
    'TP53  ',
    'TP53  dec exp',
    'TP53  inact mut',
    'TP53 C176F ',
    'TP53 E298* ',
    'TP53 G105C ',
    'TP53 N30fs*14 ',
    'TP53 P177T ',
    'TP53 Q192K ',
    'TP53 R158H ',
    'TP53 R248L ',
    'TP53 R273H ',
    'TP53 R306* ',
    'TP53 R335fs ',
    'TP53 S127Y ',
    'TP53 S241F ',
    'TP53 S90fs*33 ',
    'TP53 T118Qfs*5 ',
    'TP53 V157fs ',
    'TP53 V216M ',
    'TP53 Y220C ',
    'VHL  loss',
]


def test_cosmic_lookup_table():
    for profile in JAX_FEATURES:
        gene_index, mut_index, biomarkers, fusions = jax._parse_profile(profile)
        if not (len(gene_index) == len(mut_index) == len(biomarkers)):
            print(
                "ERROR: This molecular profile has been parsed incorrectly!")
            print(json.dumps(
                {"molecular_profile": profile},
                indent=2, sort_keys=True))
            print gene_index, mut_index, biomarkers, fusions


def test_misses():
    MISSES = ['FGFR3 Y375C', 'FGFR2 M538I', 'FGFR2 C383R', 'FGFR3 K652E', 'FGFR3 G372C']
    for profile in MISSES:
        gene_index, mut_index, biomarkers, fusions = jax._parse_profile(profile)
        if not (len(gene_index) == len(mut_index) == len(biomarkers)):
            print(
                "ERROR: This molecular profile has been parsed incorrectly!")
            print(json.dumps(
                {"molecular_profile": profile},
                indent=2, sort_keys=True))
        print gene_index, mut_index, biomarkers, fusions
        matches = LOOKUP_TABLE.get_entries(gene_index[0], mut_index[0])
        print matches
        break
