'''
    test case no: WB.PF.50
    test setup: MMEPOOL open;
                cell active,mme connect
                SA2,SSP7 20M NAT
'''
import os
import logging
from common import *
from webset import *
from config import *

class DoTest():
    def __init__(self,args,ueargs):
        self.args = args
        self.ueargs = ueargs
        self.logger = logging.getLogger('test')
        self.logger.info("Args is %s" % self.args)
        self.logger.info("Ue args is %s" % self.ueargs)
    
    def _setup(self):
        '''
         Setup before starting test
        '''
        self.cpeiplist = GetConfig.get_cpeiplist(self.ueargs)
        self.logger.info("cpeiplist is %s " % self.cpeiplist)
        self.ftpiplist = GetConfig.get_ftpiplist(self.ueargs)
        self.logger.info("ftpiplist is %s" % self.ftpiplist)
        self.logger.info("mmepool enable setting")
        ipseclist = GetConfig.get_config("MMEPOOL","TWOTUNNEL")
        self.logger.info("ipseclist is %s" % ipseclist)
        mmelist = GetConfig.get_config("MMEPOOL","MMEPOOLIP")
        self.logger.info("mmelist is %s" % mmelist)
        qslist = GetConfig.get_config("MMEPOOL","QSMMEPOOL37")
        self.logger.info("qseting args is %s" % qslist)
        self.mmeerrorip = GetConfig.get_config("MMEPOOL","MMEERRORROUTE")
        self.mmeips = GetConfig.get_config("MMEPOOL","MMEIPS")
        self.logger.info("mmeips is %s" % self.mmeips)
        test = LmtSeting("http://%s" %self.args["chost"])
        test.login_lmt()
        test.mmepool_enable_setting(ipseclist,mmelist,qslist[0])
        test.lgw_setting(["1","NAT"])
        test.do_reboot()
        test.tear_down()


    def _dotest(self):
        test = LmtCheck("http://%s" % self.args["chost"])
        test.login_lmt()
        test.check_cell_state("Active")
        test.check_mme_state("2")
        test.tear_down()
        job = TestPerformance()
        self.logger.info("start ping test")
        result = job.uepingtest([self.ftpiplist[0]]) # one cpe 
        if result:
            self.logger.info("ftp ping is pass")
        else:
            self.logger.info("ping ftp fail")
            return False
        # tcp up test
        status=job.iperf_stress_test("UP","TCP",120)
        # tcp down test
        status=job.iperf_stress_test("DOWN","TCP",120)
    
    def _runtest(self):
        self._setup()
        times = 1
        failtime = 0
        for i in range(times):
            self.logger.info("The No. %s test start" % i)
            status = self._dotest()
            if status:
                self.logger.info("The No. %s test pass" % i)
            else:
                self.logger.info("The No. %s test fail" % i)
                failtime +=1
        if failtime > 0:
            self.logger.error("WB.PF.50 is test Fail")
            return "Fail"
        else:
            self.logger.info("WB.PF.50 is test Pass")
            return "Pass"

    def _tear_down(self,browser):
        browser._tear_down()
        
        
        
        
    
                                  
        
        


        


	     

