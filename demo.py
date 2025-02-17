import argparse
import pathlib
import cv2
import time
import torch
import csv
import os
from l2cs import select_device, Pipeline, render


# PIPELINE NOTICE: I have mistakenly processed the frames at a rate of 10 FPS with videos ending in "_gaze_data-sw"(all completed before PMAR13), "-sw_bb"(all completed), and "-ms_bb"(all completed before HKHR12)
# To make it 3 fps, you must process these videos by intervals of 10 frames as they are a total of 8550 frames. --> refer to csv files of "_gaze_raw" and "_bound" respectively


CWD = pathlib.Path.cwd()
sw_files = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-sw.mp4","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-sw.mp4",-->finished!
     "AJMZ11":"../BBN_test_D_Spikol/AJMZ11/AJMZ11-sw.mp4",
     "BARB14":"../BBN_test_D_Spikol/BARB14/BARB14-sw.mp4","BARR11":"../BBN_test_D_Spikol/BARR11/BARR11-sw.mp4",
     "BATC18":"../BBN_test_D_Spikol/BATC18/BATC18-sw.mp4","BESE11":"../BBN_test_D_Spikol/BESE11/BESE11-sw.mp4",
     "BJHM14":"../BBN_test_D_Spikol/BJHM14/BJHM14-sw.mp4",
     "BJSS12":"../BBN_test_D_Spikol/BJSS12/BJSS12-sw.mp4",
     "BNTS11":"../BBN_test_D_Spikol/BNTS11/BNTS11-sw.mp4","CAMB12":"../BBN_test_D_Spikol/CAMB12/CAMB12-sw.mp4",
     "CCMJ13":"../BBN_test_D_Spikol/CCMJ13/CCMJ13-sw.mp4","CJDL17":"../BBN_test_D_Spikol/CJDL17/CJDL17-sw.mp4",
     "CKGM11":"../BBN_test_D_Spikol/CKGM11/CKGM11-sw.mp4","CKPS18":"../BBN_test_D_Spikol/CKPS18/CKPS18-sw.mp4",
     "CMMS11":"../BBN_test_D_Spikol/CMMS11/CMMS11-sw.mp4","CNIP":"../BBN_test_D_Spikol/CNIP/CNIP-sw.mp4",
     "DBCH18":"../BBN_test_D_Spikol/DBCH18/DBCH18-sw.mp4","DBJH13":"../BBN_test_D_Spikol/DBJH13/DBJH13-sw.mp4",
     "DHKM13":"../BBN_test_D_Spikol/DHKM13/DHKM13-sw.mp4",
     "DHPL12":"../BBN_test_D_Spikol/DHPL12/DHPL12-sw.mp4",
     "DRBR12":"../BBN_test_D_Spikol/DRBR12/DRBR12-sw.mp4",
     "EBLK17":"../BBN_test_D_Spikol/EBLK17/EBLK17-sw.mp4",
     "FAMJ18":"../BBN_test_D_Spikol/FAMJ18/FAMJ18-sw.mp4","FBSJ12":"../BBN_test_D_Spikol/FBSJ12/FBSJ12-sw.mp4",
     "FDBS12":"../BBN_test_D_Spikol/FDBS12/FDBS12-sw.mp4","FHTS12":"../BBN_test_D_Spikol/FHTS12/FHTS12-sw.mp4",
     "GANN11":"../BBN_test_D_Spikol/GANN11/GANN11-sw.mp4","GDPM18":"../BBN_test_D_Spikol/GDPM18/GDPM18-sw.mp4",
     "GGRR18":"../BBN_test_D_Spikol/GGRR18/GGRR18-sw.mp4","GJOK12":"../BBN_test_D_Spikol/GJOK12/GJOK12-sw.mp4",
     "GKIM11":"../BBN_test_D_Spikol/GKIM11/GKIM11-sw.mp4","GKLS17":"../BBN_test_D_Spikol/GKLS17/GKLS17-sw.mp4",
     "HAAM11":"../BBN_test_D_Spikol/HAAM11/HAAM11-sw.mp4","HAAT12":"../BBN_test_D_Spikol/HAAT12/HAAT12-sw.mp4",
     "HACD11":"../BBN_test_D_Spikol/HACD11/HACD11-sw.mp4","HAHM13":"../BBN_test_D_Spikol/HAHM13/HAHM13-sw.mp4",
     "HAWJ12":"../BBN_test_D_Spikol/HAWJ12/HAWJ12-sw.mp4","HEPH13":"../BBN_test_D_Spikol/HEPH13/HEPH13-sw.mp4",
     "HJES12":"../BBN_test_D_Spikol/HJES12/HJES12-sw.mp4","HJLL13":"../BBN_test_D_Spikol/HJLL13/HJLL13-sw.mp4",
     "HKHR12":"../BBN_test_D_Spikol/HKHR12/HKHR12-sw.mp4","HKNS17":"../BBN_test_D_Spikol/HKNS17/HKNS17-sw.mp4",
     "HLNS11":"../BBN_test_D_Spikol/HLNS11/HLNS11-sw.mp4","HSLV11":"../BBN_test_D_Spikol/HSLV11/HSLV11-sw.mp4",
     "IMVM12":"../BBN_test_D_Spikol/IMVM12/IMVM12-sw.mp4","JCBS11":"../BBN_test_D_Spikol/JCBS11/JCBS11-sw.mp4",
     "JJFW17":"../BBN_test_D_Spikol/JJFW17/JJFW17-sw.mp4","JKPR12":"../BBN_test_D_Spikol/JKPR12/JKPR12-sw.mp4",
     "KAHH18":"../BBN_test_D_Spikol/KAHH18/KAHH18-sw.mp4","KAJJ11":"../BBN_test_D_Spikol/KAJJ11/KAJJ11-sw.mp4",
     "KASL12":"../BBN_test_D_Spikol/KASL12/KASL12-sw.mp4","KASS12":"../BBN_test_D_Spikol/KASS12/KASS12-sw.mp4",
     "KCRC11":"../BBN_test_D_Spikol/KCRC11/KCRC11-sw.mp4","KESK12":"../BBN_test_D_Spikol/KESK12/KESK12-sw.mp4",
     "KJDM17":"../BBN_test_D_Spikol/KJDM17/KJDM17-sw.mp4","KJRO12":"../BBN_test_D_Spikol/KJRO12/KJRO12-sw.mp4",
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11-sw.mp4","LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13-sw.mp4",
     "LJLS12":"../BBN_test_D_Spikol/LJLS12/LJLS12-sw.mp4","LMMS15":"../BBN_test_D_Spikol/LMMS15/LMMS15-sw.mp4",
     "LNNN12":"../BBN_test_D_Spikol/LNNN12/LNNN12-sw.mp4","MAHE12":"../BBN_test_D_Spikol/MAHE12/MAHE12-sw.mp4",
     "MASM11":"../BBN_test_D_Spikol/MASM11/MASM11-sw.mp4","MCAS18":"../BBN_test_D_Spikol/MCAS18/MCAS18-sw.mp4",
     "MDHM18":"../BBN_test_D_Spikol/MDHM18/MDHM18-sw.mp4","MEGP13":"../BBN_test_D_Spikol/MEGP13/MEGP13-sw.mp4",
     "MHAS16":"../BBN_test_D_Spikol/MHAS16/MHAS16-sw.mp4","MJMM18":"../BBN_test_D_Spikol/MJMM18/MJMM18-sw.mp4",
     "MJPN13":"../BBN_test_D_Spikol/MJPN13/MJPN13-sw.mp4","MJRM17":"../BBN_test_D_Spikol/MJRM17/MJRM17-sw.mp4",
     "MJSK13":"../BBN_test_D_Spikol/MJSK13/MJSK13-sw.mp4","MJSM13":"../BBN_test_D_Spikol/MJSM13/MJSM13-sw.mp4",
     "MJTR16":"../BBN_test_D_Spikol/MJTR16/MJTR16-sw.mp4","MLHZ12":"../BBN_test_D_Spikol/MLHZ12/MLHZ12-sw.mp4",
     "MMRN13":"../BBN_test_D_Spikol/MMRN13/MMRN13-sw.mp4","MMSN12":"../BBN_test_D_Spikol/MMSN12/MMSN12-sw.mp4",
     "NADJ12":"../BBN_test_D_Spikol/NADJ12/NADJ12-sw.mp4","NCFE18":"../BBN_test_D_Spikol/NCFE18/NCFE18-sw.mp4",
     "NFAR12":"../BBN_test_D_Spikol/NFAR12/NFAR12-sw.mp4","NKTM18":"../BBN_test_D_Spikol/NKTM18/NKTM18-sw.mp4",
    #  "NKTO17":"../BBN_test_D_Spikol/NKTO17/NKTO17-sw.mp4", --> LLM POLICY ISSUE
     "PCFN14":"../BBN_test_D_Spikol/PCFN14/PCFN14-sw.mp4",
     "PGSN18":"../BBN_test_D_Spikol/PGSN18/PGSN18-sw.mp4","PJMR16":"../BBN_test_D_Spikol/PJMR16/PJMR16-sw.mp4",
     "PJPK13":"../BBN_test_D_Spikol/PJPK13/PJPK13-sw.mp4","PKBK17":"../BBN_test_D_Spikol/PKBK17/PKBK17-sw.mp4",
     "PLDX18":"../BBN_test_D_Spikol/PLDX18/PLDX18-sw.mp4","PMAR13":"../BBN_test_D_Spikol/PMAR13/PMAR13-sw.mp4",
     "RABN11":"../BBN_test_D_Spikol/RABN11/RABN11-sw.mp4","RAPS13":"../BBN_test_D_Spikol/RAPS13/RAPS13-sw.mp4",
     "REAS17":"../BBN_test_D_Spikol/REAS17/REAS17-sw.mp4","RJKR11":"../BBN_test_D_Spikol/RJKR11/RJKR11-sw.mp4",
     "RJOJ13":"../BBN_test_D_Spikol/RJOJ13/RJOJ13-sw.mp4","RNAS17":"../BBN_test_D_Spikol/RNAS17/RNAS17-sw.mp4",
     "SAFD17":"../BBN_test_D_Spikol/SAFD17/SAFD17-sw.mp4","SAFM":"../BBN_test_D_Spikol/SAFM/SAFM-sw.mp4",
     "SAHC18":"../BBN_test_D_Spikol/SAHC18/SAHC18-sw.mp4","SAJN11":"../BBN_test_D_Spikol/SAJN11/SAJN11-sw.mp4",
     "SALM18":"../BBN_test_D_Spikol/SALM18/SALM18-sw.mp4","SAPW12":"../BBN_test_D_Spikol/SAPW12/SAPW12-sw.mp4",
     "SARE13":"../BBN_test_D_Spikol/SARE13/SARE13-sw.mp4","SASS11":"../BBN_test_D_Spikol/SASS11/SASS11-sw.mp4",
     "SAYN17":"../BBN_test_D_Spikol/SAYN17/SAYN17-sw.mp4","SBHS":"../BBN_test_D_Spikol/SBHS/SBHS-sw.mp4",
     "SCBS18":"../BBN_test_D_Spikol/SCBS18/SCBS18-sw.mp4","SCFL13":"../BBN_test_D_Spikol/SCFL13/SCFL13-sw.mp4",
     "SCJN17":"../BBN_test_D_Spikol/SCJN17/SCJN17-sw.mp4","SDAE14":"../BBN_test_D_Spikol/SDAE14/SDAE14-sw.mp4",
     "SDMM13":"../BBN_test_D_Spikol/SDMM13/SDMM13-sw.mp4","SEFI13":"../BBN_test_D_Spikol/SEFI13/SEFI13-sw.mp4",
     "SEGH11":"../BBN_test_D_Spikol/SEGH11/SEGH11-sw.mp4","SEKS18":"../BBN_test_D_Spikol/SEKS18/SEKS18-sw.mp4",
     "SHHM18":"../BBN_test_D_Spikol/SHHM18/SHHM18-sw.mp4","SIAP17":"../BBN_test_D_Spikol/SIAP17/SIAP17-sw.mp4",
     "SJGK17":"../BBN_test_D_Spikol/SJGK17/SJGK17-sw.mp4","SJNA":"../BBN_test_D_Spikol/SJNA/SJNA-sw.mp4",
     "SKWN16":"../BBN_test_D_Spikol/SKWN16/SKWN16-sw.mp4",
      # "SLFS17":"../BBN_test_D_Spikol/SLFS17/SLFS17-sw.mp4", --> LLM POLICY ISSUE
     "SMZT17":"../BBN_test_D_Spikol/SMZT17/SMZT17-sw.mp4","TEOS13":"../BBN_test_D_Spikol/TEOS13/TEOS13-sw.mp4",
     "VCPS13":"../BBN_test_D_Spikol/VCPS13/VCPS13-sw.mp4","WAGD18":"../BBN_test_D_Spikol/WAGD18/WAGD18-sw.mp4",
     "WASE17":"../BBN_test_D_Spikol/WASE17/WASE17-sw.mp4","WCSV18":"../BBN_test_D_Spikol/WCSV18/WCSV18-sw.mp4",
     "WJCM17":"../BBN_test_D_Spikol/WJCM17/WJCM17-sw.mp4","WJGK17":"../BBN_test_D_Spikol/WJGK17/WJGK17-sw.mp4",
     "WMHR13":"../BBN_test_D_Spikol/WMHR13/WMHR13-sw.mp4","YBBL11":"../BBN_test_D_Spikol/YBBL11/YBBL11-sw.mp4",
     "ZABG13":"../BBN_test_D_Spikol/ZABG13/ZABG13-sw.mp4","ZCSS18":"../BBN_test_D_Spikol/ZCSS18/ZCSS18-sw.mp4",
     "ZNBS12":"../BBN_test_D_Spikol/ZNBS12/ZNBS12-sw.mp4"}

ms_files = {
    # "HCAJ18":"../BBN_test_D_Spikol/HCAJ18/HCAJ18-ms.mp4","KEMK18":"../BBN_test_D_Spikol/KEMK18/KEMK18-ms.mp4",
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
     "KKMM11":"../BBN_test_D_Spikol/KKMM11/KKMM11-ms.mp4",
     "LEMM13":"../BBN_test_D_Spikol/LEMM13/LEMM13-ms.mp4",
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

def parse_args():
    parser = argparse.ArgumentParser(description='Gaze evaluation using model pretrained with L2CS-Net on Gaze360.')
    parser.add_argument('--device', help='Device to run model: cpu or gpu:0', default='cpu', type=str)
    parser.add_argument('--snapshot', help='Path of model snapshot.', default='output/L2CSNet_gaze360.pkl', type=str)
    parser.add_argument('--output_dir', help='Directory to save csv files.', default='output_csv', type=str)
    parser.add_argument('--arch', help='Network architecture, can be: ResNet18, ResNet34, ResNet50, ResNet101, ResNet152', default='ResNet50', type=str)
    
    args = parser.parse_args()
    return args

def draw_headbox(frame, bbox, color=(0, 255, 0), thickness=2):
    x, y, w, h = map(int, bbox)
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

def render(frame, gaze_results_container):
    try:
        for i, bbox in enumerate(gaze_results_container.bboxes):
            print(f"Rendered bbox: {bbox}")

            score = gaze_results_container.scores[i]
            pitch = gaze_results_container.pitch[i]
            yaw = gaze_results_container.yaw[i]

            draw_headbox(frame, bbox)

            text = f'Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Score: {score:.2f}'
            cv2.putText(frame, text, (int(bbox[0]), int(bbox[1]) - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (0, 255, 0), 1)
    except Exception as e:
        print(f"Error in rendering the frame: {e}")
    return frame

def process_video(video_path, output_csv_path, output_video_path, gaze_pipeline):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")

    frame_numbers_to_process = range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 10)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), 3, (width, height))

    with open(output_csv_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Frame', 'x', 'y', 'width', 'height', 'Pitch', 'Yaw', 'Score'])

        with torch.no_grad():
            frame_count = 0
            
            while True:
                success, frame = cap.read()
                if not success:
                    print("Failed to obtain frame or end of video.")
                    break
                
                if frame_count not in frame_numbers_to_process:
                    frame_count += 1
                    continue

                start_fps = time.time()
                results = gaze_pipeline.step(frame)
                frame = render(frame, results)

                for i, bbox in enumerate(results.bboxes):
                    score = results.scores[i]
                    pitch = results.pitch[i]
                    yaw = results.yaw[i]
                    x, y, w, h = map(int, bbox)
                    csv_writer.writerow([frame_count, x, y, w, h, pitch, yaw, score])

                frame_count += 1

                myFPS = 1.0 / (time.time() - start_fps)
                cv2.putText(frame, f'FPS: {myFPS:.1f}', (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1, cv2.LINE_AA)

                out.write(frame)

    cap.release()
    out.release()

if __name__ == '__main__':
    args = parse_args()
    torch.backends.cudnn.enabled = True
    arch = args.arch

    gaze_pipeline = Pipeline(
        weights=CWD / args.snapshot,
        arch=args.arch,
        device=select_device(args.device, batch_size=1)
    )

    # for name, video_path in sw_files.items():
    #     print(f"Processing {name}...")
    #     video_dir = os.path.dirname(video_path)  # Get the directory of the video
    #     output_csv_path = os.path.join(video_dir, f'{name}_gaze_raw-sw.csv') # Save CSV in the same directory
    #     output_video_path = os.path.join(args.output_dir, f'{name}_output.avi')
    #     process_video(video_path, output_csv_path, output_video_path, gaze_pipeline)
    #     print(f"Finished processing {name}. CSV saved to {output_csv_path}, video saved to {output_video_path}")
        
    for name, video_path in ms_files.items():
        print(f"Processing {name}...")
        video_dir = os.path.dirname(video_path)  # Get the directory of the video
        output_csv_path = os.path.join(video_dir, f'{name}_gaze_raw-ms.csv') # Save CSV in the same directory
        output_video_path = os.path.join(args.output_dir, f'{name}_output.avi')
        process_video(video_path, output_csv_path, output_video_path, gaze_pipeline)
        print(f"Finished processing {name}. CSV saved to {output_csv_path}, video saved to {output_video_path}")