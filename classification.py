from collections import OrderedDict
import csv
import pandas as pd
import cv2
import os

sw_body = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-sw_bound.csv","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-sw_bound.csv",-->finished!
    #  "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11-sw_bound.csv",
    #  "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14-sw_bound-revised.csv","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11-sw_bound-revised.csv",
    #  "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18-sw_bound-revised.csv","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11-sw_bound-revised.csv",
    #  "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14-sw_bound-revised.csv",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12-sw_bound-revised2.csv",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11-sw_bound-revised2.csv","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12-sw_bound-revised2.csv",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13-sw_bound-revised2.csv","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17-sw_bound-revised2.csv",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11-sw_bound-revised2.csv","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18-sw_bound-revised2.csv",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11-sw_bound-revised2.csv","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP-sw_bound-revised2.csv",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18-sw_bound-revised2.csv","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13-sw_bound-revised2.csv",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13-sw_bound-revised2.csv",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12-sw_bound-revised2.csv",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12-sw_bound-revised2.csv",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17-sw_bound-revised2.csv",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18-sw_bound-revised2.csv","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12-sw_bound-revised2.csv",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12-sw_bound-revised2.csv","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12-sw_bound-revised2.csv",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11-sw_bound-revised2.csv","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18-sw_bound-revised2.csv",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18-sw_bound-revised2.csv","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12-sw_bound-revised2.csv",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11-sw_bound-revised2.csv","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17-sw_bound-revised2.csv",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11-sw_bound-revised2.csv","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12-sw_bound-revised2.csv",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11-sw_bound-revised2.csv","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13-sw_bound-revised2.csv",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12-sw_bound-revised2.csv","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13-sw_bound-revised2.csv",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12-sw_bound-revised2.csv","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13-sw_bound-revised2.csv",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12-sw_bound-revised2.csv","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17-sw_bound-revised2.csv",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11-sw_bound-revised2.csv","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11-sw_bound-revised2.csv",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12-sw_bound-revised2.csv","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11-sw_bound-revised2.csv",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17-sw_bound-revised2.csv","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12-sw_bound-revised2.csv",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18-sw_bound-revised2.csv","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11-sw_bound-revised2.csv",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12-sw_bound-revised2.csv","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12-sw_bound-revised2.csv",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11-sw_bound-revised2.csv", 
     "KESK12":"../BBN_test_D_Spikol/KESK12/KESK12-sw_bound-revised2.csv",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17-sw_bound-revised2.csv","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12-sw_bound-revised2.csv",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11-sw_bound-revised2.csv","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13-sw_bound-revised2.csv",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12-sw_bound-revised2.csv","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15-sw_bound-revised2.csv",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12-sw_bound-revised2.csv","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12-sw_bound-revised2.csv",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11-sw_bound-revised2.csv","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18-sw_bound-revised2.csv",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18-sw_bound-revised2.csv",
     "MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13-sw_bound-revised2.csv",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16-sw_bound-revised2.csv", 
     "MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18-sw_bound-revised2.csv",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13-sw_bound-revised2.csv","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17-sw_bound-revised2.csv",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13-sw_bound-revised2.csv","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13-sw_bound-revised2.csv",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16-sw_bound-revised2.csv","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12-sw_bound-revised2.csv",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13-sw_bound-revised2.csv","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12-sw_bound-revised2.csv",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12-sw_bound-revised2.csv","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18-sw_bound-revised2.csv",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12-sw_bound-revised2.csv","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18-sw_bound-revised2.csv",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17-sw_bound-revised2.csv", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14-sw_bound-revised2.csv",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18-sw_bound-revised2.csv","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16-sw_bound-revised2.csv",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13-sw_bound-revised2.csv","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17-sw_bound-revised2.csv",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18-sw_bound-revised2.csv","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13-sw_bound-revised2.csv",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11-sw_bound-revised2.csv","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13-sw_bound-revised2.csv",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17-sw_bound-revised2.csv","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11-sw_bound-revised2.csv",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13-sw_bound-revised2.csv","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17-sw_bound-revised2.csv",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17-sw_bound-revised2.csv","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM-sw_bound-revised2.csv",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18-sw_bound-revised2.csv","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11-sw_bound-revised2.csv",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18-sw_bound-revised2.csv","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12-sw_bound-revised2.csv",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13-sw_bound-revised2.csv","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11-sw_bound-revised2.csv",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17-sw_bound-revised2.csv","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS-sw_bound-revised2.csv",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18-sw_bound-revised2.csv","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13-sw_bound-revised2.csv",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17-sw_bound-revised2.csv","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14-sw_bound-revised2.csv",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13-sw_bound-revised2.csv","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13-sw_bound-revised2.csv",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11-sw_bound-revised2.csv","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18-sw_bound-revised2.csv",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18-sw_bound-revised2.csv","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17-sw_bound-revised2.csv",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17-sw_bound-revised2.csv","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA-sw_bound-revised2.csv",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16-sw_bound-revised2.csv",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17-sw_bound-revised2.csv", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17-sw_bound-revised2.csv","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13-sw_bound-revised2.csv",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13-sw_bound-revised2.csv","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18-sw_bound-revised2.csv",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17-sw_bound-revised2.csv","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18-sw_bound-revised2.csv",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17-sw_bound-revised2.csv","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17-sw_bound-revised2.csv",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13-sw_bound-revised2.csv","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11-sw_bound-revised2.csv",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13-sw_bound-revised2.csv","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18-sw_bound-revised2.csv",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12-sw_bound-revised2.csv"}

sw_faces = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-sw_bound.csv","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-sw_bound.csv",-->finished!
     "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11_gaze_raw-sw.csv",
     "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14_gaze_raw-sw.csv","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11_gaze_raw-sw.csv",
     "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18_gaze_raw-sw.csv","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11_gaze_raw-sw.csv",
     "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14_gaze_raw-sw.csv",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12_gaze_raw-sw.csv",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11_gaze_raw-sw.csv","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12_gaze_raw-sw.csv",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13_gaze_raw-sw.csv","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17_gaze_raw-sw.csv",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11_gaze_raw-sw.csv","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18_gaze_raw-sw.csv",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11_gaze_raw-sw.csv","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP_gaze_raw-sw.csv",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18_gaze_raw-sw.csv","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13_gaze_raw-sw.csv",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13_gaze_raw-sw.csv",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12_gaze_raw-sw.csv",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12_gaze_raw-sw.csv",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17_gaze_raw-sw.csv",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18_gaze_raw-sw.csv","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12_gaze_raw-sw.csv",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12_gaze_raw-sw.csv","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12_gaze_raw-sw.csv",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11_gaze_raw-sw.csv","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18_gaze_raw-sw.csv",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18_gaze_raw-sw.csv","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12_gaze_raw-sw.csv",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11_gaze_raw-sw.csv","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17_gaze_raw-sw.csv",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11_gaze_raw-sw.csv","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12_gaze_raw-sw.csv",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11_gaze_raw-sw.csv","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13_gaze_raw-sw.csv",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12_gaze_raw-sw.csv","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13_gaze_raw-sw.csv",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12_gaze_raw-sw.csv","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13_gaze_raw-sw.csv",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12_gaze_raw-sw.csv","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17_gaze_raw-sw.csv",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11_gaze_raw-sw.csv","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11_gaze_raw-sw.csv",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12_gaze_raw-sw.csv","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11_gaze_raw-sw.csv",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17_gaze_raw-sw.csv","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12_gaze_raw-sw.csv",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18_gaze_raw-sw.csv","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11_gaze_raw-sw.csv",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12_gaze_raw-sw.csv","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12_gaze_raw-sw.csv",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11_gaze_raw-sw.csv", 
     "KESK12":"../BBN_test_D_Spikol/KESK12/KESK12_gaze_raw-sw.csv",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17_gaze_raw-sw.csv","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12_gaze_raw-sw.csv",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11_gaze_raw-sw.csv","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13_gaze_raw-sw.csv",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12_gaze_raw-sw.csv","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15_gaze_raw-sw.csv",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12_gaze_raw-sw.csv","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12_gaze_raw-sw.csv",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11_gaze_raw-sw.csv","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18_gaze_raw-sw.csv",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18_gaze_raw-sw.csv",
     "MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13_gaze_raw-sw.csv",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16_gaze_raw-sw.csv", 
     "MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18_gaze_raw-sw.csv",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13_gaze_raw-sw.csv","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17_gaze_raw-sw.csv",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13_gaze_raw-sw.csv","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13_gaze_raw-sw.csv",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16_gaze_raw-sw.csv","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12_gaze_raw-sw.csv",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13_gaze_raw-sw.csv","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12_gaze_raw-sw.csv",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12_gaze_raw-sw.csv","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18_gaze_raw-sw.csv",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12_gaze_raw-sw.csv","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18_gaze_raw-sw.csv",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17_gaze_raw-sw.csv", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14_gaze_raw-sw.csv",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18_gaze_raw-sw.csv","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16_gaze_raw-sw.csv",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13_gaze_raw-sw.csv","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17_gaze_raw-sw.csv",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18_gaze_raw-sw.csv","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13_gaze_raw-sw.csv",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11_gaze_raw-sw.csv","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13_gaze_raw-sw.csv",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17_gaze_raw-sw.csv","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11_gaze_raw-sw.csv",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13_gaze_raw-sw.csv","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17_gaze_raw-sw.csv",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17_gaze_raw-sw.csv","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM_gaze_raw-sw.csv",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18_gaze_raw-sw.csv","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11_gaze_raw-sw.csv",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18_gaze_raw-sw.csv","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12_gaze_raw-sw.csv",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13_gaze_raw-sw.csv","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11_gaze_raw-sw.csv",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17_gaze_raw-sw.csv","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS_gaze_raw-sw.csv",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18_gaze_raw-sw.csv","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13_gaze_raw-sw.csv",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17_gaze_raw-sw.csv","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14_gaze_raw-sw.csv",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13_gaze_raw-sw.csv","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13_gaze_raw-sw.csv",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11_gaze_raw-sw.csv","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18_gaze_raw-sw.csv",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18_gaze_raw-sw.csv","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17_gaze_raw-sw.csv",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17_gaze_raw-sw.csv","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA_gaze_raw-sw.csv",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16_gaze_raw-sw.csv",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17_gaze_raw-sw.csv", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17_gaze_raw-sw.csv","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13_gaze_raw-sw.csv",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13_gaze_raw-sw.csv","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18_gaze_raw-sw.csv",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17_gaze_raw-sw.csv","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18_gaze_raw-sw.csv",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17_gaze_raw-sw.csv","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17_gaze_raw-sw.csv",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13_gaze_raw-sw.csv","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11_gaze_raw-sw.csv",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13_gaze_raw-sw.csv","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18_gaze_raw-sw.csv",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12_gaze_raw-sw.csv"}

ms_body = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-ms_bound.csv","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-ms_bound.csv",-->finished!
    #  "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11-ms_bound.csv",
     "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14-ms_bound-revised2.csv","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11-ms_bound-revised2.csv",
     "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18-ms_bound-revised2.csv","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11-ms_bound-revised2.csv",
     "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14-ms_bound-revised2.csv",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12-ms_bound-revised2.csv",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11-ms_bound-revised2.csv","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12-ms_bound-revised2.csv",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13-ms_bound-revised2.csv","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17-ms_bound-revised2.csv",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11-ms_bound-revised2.csv","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18-ms_bound-revised2.csv",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11-ms_bound-revised2.csv","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP-ms_bound-revised2.csv",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18-ms_bound-revised2.csv","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13-ms_bound-revised2.csv",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13-ms_bound-revised2.csv",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12-ms_bound-revised2.csv",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12-ms_bound-revised2.csv",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17-ms_bound-revised2.csv",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18-ms_bound-revised2.csv","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12-ms_bound-revised2.csv",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12-ms_bound-revised2.csv","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12-ms_bound-revised2.csv",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11-ms_bound-revised2.csv","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18-ms_bound-revised2.csv",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18-ms_bound-revised2.csv","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12-ms_bound-revised2.csv",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11-ms_bound-revised2.csv","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17-ms_bound-revised2.csv",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11-ms_bound-revised2.csv","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12-ms_bound-revised2.csv",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11-ms_bound-revised2.csv","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13-ms_bound-revised2.csv",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12-ms_bound-revised2.csv","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13-ms_bound-revised2.csv",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12-ms_bound-revised2.csv","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13-ms_bound-revised2.csv",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12-ms_bound-revised2.csv","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17-ms_bound-revised2.csv",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11-ms_bound-revised2.csv","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11-ms_bound-revised2.csv",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12-ms_bound-revised2.csv","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11-ms_bound-revised2.csv",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17-ms_bound-revised2.csv","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12-ms_bound-revised2.csv",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18-ms_bound-revised2.csv","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11-ms_bound-revised2.csv",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12-ms_bound-revised2.csv","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12-ms_bound-revised2.csv",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11-ms_bound-revised2.csv","KESK12":"../BBN_test_D_Spikol/KESK12/KESK12-ms_bound-revised2.csv",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17-ms_bound-revised2.csv","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12-ms_bound-revised2.csv",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11-ms_bound-revised2.csv","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13-ms_bound-revised2.csv",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12-ms_bound-revised2.csv","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15-ms_bound-revised2.csv",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12-ms_bound-revised2.csv","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12-ms_bound-revised2.csv",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11-ms_bound-revised2.csv","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18-ms_bound-revised2.csv",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18-ms_bound-revised2.csv","MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13-ms_bound-revised2.csv",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16-ms_bound-revised2.csv","MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18-ms_bound-revised2.csv",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13-ms_bound-revised2.csv","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17-ms_bound-revised2.csv",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13-ms_bound-revised2.csv","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13-ms_bound-revised2.csv",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16-ms_bound-revised2.csv","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12-ms_bound-revised2.csv",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13-ms_bound-revised2.csv","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12-ms_bound-revised2.csv",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12-ms_bound-revised2.csv","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18-ms_bound-revised2.csv",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12-ms_bound-revised2.csv","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18-ms_bound-revised2.csv",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17-ms_bound-revised2.csv", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14-ms_bound-revised2.csv",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18-ms_bound-revised2.csv","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16-ms_bound-revised2.csv",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13-ms_bound-revised2.csv","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17-ms_bound-revised2.csv",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18-ms_bound-revised2.csv","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13-ms_bound-revised2.csv",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11-ms_bound-revised2.csv","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13-ms_bound-revised2.csv",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17-ms_bound-revised2.csv","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11-ms_bound-revised2.csv",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13-ms_bound-revised2.csv","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17-ms_bound-revised2.csv",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17-ms_bound-revised2.csv","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM-ms_bound-revised2.csv",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18-ms_bound-revised2.csv","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11-ms_bound-revised2.csv",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18-ms_bound-revised2.csv","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12-ms_bound-revised2.csv",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13-ms_bound-revised2.csv","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11-ms_bound-revised2.csv",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17-ms_bound-revised2.csv","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS-ms_bound-revised2.csv",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18-ms_bound-revised2.csv","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13-ms_bound-revised2.csv",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17-ms_bound-revised2.csv","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14-ms_bound-revised2.csv",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13-ms_bound-revised2.csv","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13-ms_bound-revised2.csv",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11-ms_bound-revised2.csv","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18-ms_bound-revised2.csv",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18-ms_bound-revised2.csv","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17-ms_bound-revised2.csv",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17-ms_bound-revised2.csv","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA-ms_bound-revised2.csv",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16-ms_bound-revised2.csv",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17-ms_bound-revised2.csv", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17-ms_bound-revised2.csv","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13-ms_bound-revised2.csv",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13-ms_bound-revised2.csv","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18-ms_bound-revised2.csv",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17-ms_bound-revised2.csv","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18-ms_bound-revised2.csv",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17-ms_bound-revised2.csv","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17-ms_bound-revised2.csv",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13-ms_bound-revised2.csv","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11-ms_bound-revised2.csv",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13-ms_bound-revised2.csv","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18-ms_bound-revised2.csv",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12-ms_bound-revised2.csv"}

ms_faces = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-ms_bound.csv","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-ms_bound.csv",-->finished!
     "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11_gaze_raw-ms.csv",
     "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14_gaze_raw-ms.csv","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11_gaze_raw-ms.csv",
     "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18_gaze_raw-ms.csv","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11_gaze_raw-ms.csv",
     "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14_gaze_raw-ms.csv",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12_gaze_raw-ms.csv",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11_gaze_raw-ms.csv","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12_gaze_raw-ms.csv",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13_gaze_raw-ms.csv","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17_gaze_raw-ms.csv",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11_gaze_raw-ms.csv","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18_gaze_raw-ms.csv",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11_gaze_raw-ms.csv","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP_gaze_raw-ms.csv",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18_gaze_raw-ms.csv","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13_gaze_raw-ms.csv",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13_gaze_raw-ms.csv",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12_gaze_raw-ms.csv",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12_gaze_raw-ms.csv",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17_gaze_raw-ms.csv",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18_gaze_raw-ms.csv","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12_gaze_raw-ms.csv",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12_gaze_raw-ms.csv","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12_gaze_raw-ms.csv",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11_gaze_raw-ms.csv","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18_gaze_raw-ms.csv",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18_gaze_raw-ms.csv","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12_gaze_raw-ms.csv",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11_gaze_raw-ms.csv","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17_gaze_raw-ms.csv",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11_gaze_raw-ms.csv","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12_gaze_raw-ms.csv",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11_gaze_raw-ms.csv","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13_gaze_raw-ms.csv",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12_gaze_raw-ms.csv","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13_gaze_raw-ms.csv",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12_gaze_raw-ms.csv","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13_gaze_raw-ms.csv",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12_gaze_raw-ms.csv","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17_gaze_raw-ms.csv",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11_gaze_raw-ms.csv","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11_gaze_raw-ms.csv",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12_gaze_raw-ms.csv","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11_gaze_raw-ms.csv",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17_gaze_raw-ms.csv","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12_gaze_raw-ms.csv",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18_gaze_raw-ms.csv","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11_gaze_raw-ms.csv",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12_gaze_raw-ms.csv","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12_gaze_raw-ms.csv",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11_gaze_raw-ms.csv","KESK12":"../BBN_test_D_Spikol/KESK12/KESK12_gaze_raw-ms.csv",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17_gaze_raw-ms.csv","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12_gaze_raw-ms.csv",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11_gaze_raw-ms.csv","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13_gaze_raw-ms.csv",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12_gaze_raw-ms.csv","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15_gaze_raw-ms.csv",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12_gaze_raw-ms.csv","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12_gaze_raw-ms.csv",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11_gaze_raw-ms.csv","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18_gaze_raw-ms.csv",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18_gaze_raw-ms.csv","MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13_gaze_raw-ms.csv",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16_gaze_raw-ms.csv","MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18_gaze_raw-ms.csv",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13_gaze_raw-ms.csv","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17_gaze_raw-ms.csv",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13_gaze_raw-ms.csv","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13_gaze_raw-ms.csv",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16_gaze_raw-ms.csv","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12_gaze_raw-ms.csv",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13_gaze_raw-ms.csv","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12_gaze_raw-ms.csv",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12_gaze_raw-ms.csv","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18_gaze_raw-ms.csv",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12_gaze_raw-ms.csv","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18_gaze_raw-ms.csv",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17_gaze_raw-ms.csv", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14_gaze_raw-ms.csv",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18_gaze_raw-ms.csv","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16_gaze_raw-ms.csv",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13_gaze_raw-ms.csv","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17_gaze_raw-ms.csv",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18_gaze_raw-ms.csv","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13_gaze_raw-ms.csv",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11_gaze_raw-ms.csv","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13_gaze_raw-ms.csv",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17_gaze_raw-ms.csv","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11_gaze_raw-ms.csv",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13_gaze_raw-ms.csv","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17_gaze_raw-ms.csv",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17_gaze_raw-ms.csv","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM_gaze_raw-ms.csv",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18_gaze_raw-ms.csv","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11_gaze_raw-ms.csv",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18_gaze_raw-ms.csv","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12_gaze_raw-ms.csv",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13_gaze_raw-ms.csv","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11_gaze_raw-ms.csv",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17_gaze_raw-ms.csv","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS_gaze_raw-ms.csv",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18_gaze_raw-ms.csv","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13_gaze_raw-ms.csv",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17_gaze_raw-ms.csv","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14_gaze_raw-ms.csv",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13_gaze_raw-ms.csv","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13_gaze_raw-ms.csv",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11_gaze_raw-ms.csv","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18_gaze_raw-ms.csv",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18_gaze_raw-ms.csv","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17_gaze_raw-ms.csv",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17_gaze_raw-ms.csv","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA_gaze_raw-ms.csv",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16_gaze_raw-ms.csv",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17_gaze_raw-ms.csv", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17_gaze_raw-ms.csv","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13_gaze_raw-ms.csv",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13_gaze_raw-ms.csv","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18_gaze_raw-ms.csv",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17_gaze_raw-ms.csv","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18_gaze_raw-ms.csv",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17_gaze_raw-ms.csv","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17_gaze_raw-ms.csv",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13_gaze_raw-ms.csv","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11_gaze_raw-ms.csv",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13_gaze_raw-ms.csv","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18_gaze_raw-ms.csv",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12_gaze_raw-ms.csv"}

ms_videos = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-ms_bound.csv","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-ms_bound.csv",-->finished!
     "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11-ms.mp4",
     "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14-ms.mp4","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11-ms.mp4",
     "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18-ms.mp4","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11-ms.mp4",
     "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14-ms.mp4",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12-ms.mp4",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11-ms.mp4","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12-ms.mp4",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13-ms.mp4","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17-ms.mp4",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11-ms.mp4","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18-ms.mp4",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11-ms.mp4","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP-ms.mp4",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18-ms.mp4","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13-ms.mp4",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13-ms.mp4",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12-ms.mp4",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12-ms.mp4",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17-ms.mp4",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18-ms.mp4","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12-ms.mp4",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12-ms.mp4","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12-ms.mp4",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11-ms.mp4","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18-ms.mp4",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18-ms.mp4","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12-ms.mp4",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11-ms.mp4","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17-ms.mp4",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11-ms.mp4","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12-ms.mp4",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11-ms.mp4","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13-ms.mp4",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12-ms.mp4","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13-ms.mp4",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12-ms.mp4","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13-ms.mp4",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12-ms.mp4","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17-ms.mp4",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11-ms.mp4","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11-ms.mp4",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12-ms.mp4","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11-ms.mp4",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17-ms.mp4","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12-ms.mp4",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18-ms.mp4","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11-ms.mp4",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12-ms.mp4","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12-ms.mp4",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11-ms.mp4","KESK12":"../BBN_test_D_Spikol/KESK12/KESK12-ms.mp4",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17-ms.mp4","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12-ms.mp4",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11-ms.mp4","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13-ms.mp4",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12-ms.mp4","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15-ms.mp4",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12-ms.mp4","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12-ms.mp4",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11-ms.mp4","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18-ms.mp4",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18-ms.mp4","MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13-ms.mp4",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16-ms.mp4","MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18-ms.mp4",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13-ms.mp4","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17-ms.mp4",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13-ms.mp4","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13-ms.mp4",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16-ms.mp4","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12-ms.mp4",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13-ms.mp4","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12-ms.mp4",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12-ms.mp4","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18-ms.mp4",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12-ms.mp4","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18-ms.mp4",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17-ms.mp4", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14-ms.mp4",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18-ms.mp4","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16-ms.mp4",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13-ms.mp4","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17-ms.mp4",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18-ms.mp4","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13-ms.mp4",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11-ms.mp4","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13-ms.mp4",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17-ms.mp4","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11-ms.mp4",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13-ms.mp4","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17-ms.mp4",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17-ms.mp4","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM-ms.mp4",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18-ms.mp4","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11-ms.mp4",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18-ms.mp4","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12-ms.mp4",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13-ms.mp4","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11-ms.mp4",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17-ms.mp4","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS-ms.mp4",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18-ms.mp4","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13-ms.mp4",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17-ms.mp4","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14-ms.mp4",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13-ms.mp4","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13-ms.mp4",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11-ms.mp4","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18-ms.mp4",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18-ms.mp4","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17-ms.mp4",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17-ms.mp4","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA-ms.mp4",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16-ms.mp4",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17-ms.mp4", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17-ms.mp4","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13-ms.mp4",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13-ms.mp4","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18-ms.mp4",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17-ms.mp4","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18-ms.mp4",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17-ms.mp4","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17-ms.mp4",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13-ms.mp4","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11-ms.mp4",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13-ms.mp4","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18-ms.mp4",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12-ms.mp4"}


#Insufficient FIles for classification: BJHM14, BARB14(rerun), GANN11 sw + HAHM13 sw, SLFS17, NKTO17, CJDL17(can only see sw's legs), CMMS11 ms (ms out of view), DBJH13 ms (only the ms chin can be seen), HKHR12 ms, JCBS11 ms(bounding box cannot be taken), JJFW17 (widow omitted), KAJJ11 (sw is omitted), LMMS15 + MJRM17 + ZABG13 ms (widow not seen), NADJ12, SAJN11 ms (no ms gaze), SAPW12 (sw face omitted), SDMM13 ms (sw omitted), WASE17 + DRBR12 sw + LNNN12 sw + MASM11 sw + MJSM13 sw + NADJ12 sw + PJMR16 sw + SAJN11 sw + SCFL13 sw + VCPS13 sw + ZCSS18 sw + ZNBS12 sw (no bb or lack of gaze in sw)
#potential lacks: AJMZ ms(sometimes social worker isn't bounded), BESE + CAMB ms(sw not taken for 5 minutes in BBN), DBCH18 (sw might not appear), GANN11 ms(sw gaze cannot appear w/o head), HKNS17 ms (sw omitted), IMVM12 has all info but likely innacurate, KASS12 (works but hard), LNNN12 ms (sw omitted), NCFE18 ms (sw out), PCFN14, PLDX18 ms + PMAR13 + SMZT17 ms (lack of sw gaze)
#skipping --> MDHM18 ms, MEGP13 ms

#previously revised: BJSS12 ms


           
def is_gaze_in_bbox(gaze_x, gaze_y, bbox):
    x1, y1, x2, y2 = bbox
    return x1 <= gaze_x <= x2 and y1 <= gaze_y <= y2
                
def process_files(idx):
    file_path_bound = f'../BBN_test_D_Spikol/{idx}/{idx}-sw_bound-revised2.csv'
    file_path_gaze = f'../BBN_test_D_Spikol/{idx}/{idx}_gaze_raw-sw.csv'
    output_path = f'../BBN_test_D_Spikol/{idx}/{idx}-gaze.csv'

    try:
        df_bound = pd.read_csv(file_path_bound, on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading {file_path_bound}: {e}")
        return

    try:
        df_gaze = pd.read_csv(file_path_gaze)
    except Exception as e:
        print(f"Error reading {file_path_gaze}: {e}")
        return

    df_bound['Frame'] = df_bound['Frame'].astype(int)
    df_gaze['Frame'] = df_gaze['Frame'].astype(int)

    ordered_dict = OrderedDict()

    # append the subjects
    for _, row in df_bound.iterrows():
        key = row['Frame']
        values = row[1:].tolist()

        # if the frame scene is already in there
        if key in ordered_dict:
            ordered_dict[key].append(values)
        else:
            #otherwise, we're already in a new scene frame.
            ordered_dict[key] = [values]

    with open(output_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Frame', 'Label', 'x1', 'y1', 'x2', 'y2', 'Stares At'])
        
        # each row of the csv gaze file
        for _, row in df_gaze.iterrows():
            frame = row['Frame']
            gaze_x = row['x']
            gaze_y = row['y']

            stares_at = "N/A"
            
            # only assess frames that have bb data in them
            if frame in ordered_dict:
                 for bbox in ordered_dict[frame]:
                     label = bbox[0]
                     bbox_coords = bbox[1:5]
                     if is_gaze_in_bbox(gaze_x, gaze_y, bbox_coords):
                         stares_at = label
                         break

                 for bbox in ordered_dict[frame]:
                     csv_writer.writerow([
                         frame, bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], stares_at
                     ])
    print("done with " + idx + "\n")

for idx in sw_body:
    process_files(idx)
    
    
    
    
#TASK:

#create 100 frames in random sample, have 1-2 humans to rate who is looking at who
#create a binary list --> the target of who's looking at who. (eg. 3rd class being looking at nowhere)

#make 100 frames w/o arrows --> so that they don't assume by arrows.
#don't run by script, try to find a command that does it.
#ensure frame 65, make sure it strikes that frame from the original video.