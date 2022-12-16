from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from form import Stock_Form, Buy_Sell_Stock
from data_processing import candlestick_graph, collect_stock_price

app = Flask(__name__)
app.secret_key = "Secret Key"
Bootstrap(app)

# Restricting possible stock choices to all NASDAQ companies with market value > 3 Billion Dollars
all_stocks = ['AAL', 'AAON', 'AAPL', 'AAWW', 'ABCB', 'ABCL', 'ABCM', 'ABMD', 'ABNB', 'ACAD', 'ACGL', 'ACHC', 'ACIW', 'ACLS', 'ACT', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AEIS', 'AEP', 'AFRM', 'AGNC', 'AHCO', 'AIMC', 'AKAM', 'AKRO', 'ALGM', 'ALGN', 'ALHC', 'ALKS', 'ALNY', 'ALRM', 'ALTR', 'AMAT', 'AMBA', 'AMD', 'AMED', 'AMGN', 'AMKR', 'AMLX', 'AMZN', 'ANSS', 'APA', 'APLS', 'APP', 'APPF', 'APPN', 'ARCC', 'ARGX', 'ARLP', 'ARRY', 'ARVN', 'ARWR', 'ASML', 'ASND', 'ASO', 'ATAT', 'ATRC', 'ATSG', 'ATVI', 'AUB', 'AVAV', 'AVGO', 'AVT', 'AXNX', 'AXON', 'AXSM', 'AY', 'AZN', 'AZPN', 'AZTA', 'BANF', 'BANR', 'BCPC', 'BCRX', 'BEAM', 'BECN', 'BGNE', 'BHF', 'BIDU', 'BIIB', 'BILI', 'BKNG', 'BKR', 'BL', 'BLKB', 'BMBL', 'BMRN', 'BNTX', 'BOKF', 'BPMC', 'BPOP', 'BRKR', 'BRZE', 'BSY', 'BZ', 'CACC', 'CALM', 'CAR', 'CASY', 'CATY', 'CBRL', 'CBSH', 'CCEP', 'CCOI', 'CD', 'CDNS', 'CDW', 'CEG', 'CELH', 'CENT', 'CERE', 'CERT', 'CFLT', 'CG', 'CGNX', 'CHDN', 'CHK', 'CHKP', 'CHRD', 'CHRW', 'CHTR', 'CHX', 'CIGI', 'CINF', 'CLBK', 'CMCSA', 'CME', 'CNXC', 'COHR', 'COIN', 'COKE', 'COLB', 'COLM', 'COOP', 'CORT', 'COST', 'COUP', 'CPRT', 'CRDO', 'CROX', 'CRSP', 'CRUS', 'CRVL', 'CRWD', 'CSCO', 'CSGP', 'CSIQ', 'CSQ', 'CSX', 'CTAS', 'CTSH', 'CVBF', 'CVCO', 'CVLT', 'CVT', 'CWST', 'CYBR', 'CYTK', 'CZR', 'DADA', 'DBX', 'DDOG', 'DIOD', 'DISH', 'DKNG', 'DLO', 'DLTR', 'DNLI', 'DNUT', 'DOCU', 'DOOO', 'DORM', 'DOX', 'DRVN', 'DSGX', 'DUOL', 'DXCM', 'EA', 'EBAY', 'EBC', 'EEFT', 'EMBC', 'ENPH', 'ENSG', 'ENTG', 'EQIX', 'ERIC', 'ERIE', 'ESGR', 'ESLT', 'ETSY', 'EVO', 'EWBC', 'EXAS', 'EXC', 'EXEL', 'EXLS', 'EXPD', 'EXPE', 'EXPO', 'EXTR', 'EYE', 'FA', 'FANG', 'FAST', 'FCFS', 'FCNCA', 'FELE', 'FFBC', 'FFIN', 'FFIV', 'FHB', 'FIBK', 'FISV', 'FITB', 'FIVE', 'FIVN', 'FIZZ', 'FLEX', 'FLNC', 'FLYW', 'FOCS', 'FOLD', 'FOX', 'FOXA', 'FOXF', 'FRHC', 'FRME', 'FROG', 'FRPT', 'FRSH', 'FSLR', 'FSV', 'FTNT', 'FULT', 'FUTU', 'FWONA', 'FWONK', 'FWRD', 'FYBR', 'GBDC', 'GDRX', 'GDS', 'GEN', 'GFS', 'GH', 'GILD', 'GLBE', 'GLNG', 'GLPG', 'GLPI', 'GMAB', 'GNTX', 'GO', 'GOOG', 'GOOGL', 'GRAB', 'GRFS', 'GT', 'GTLB', 'HALO', 'HAS', 'HBAN', 'HCM', 'HCP', 'HELE', 'HLNE', 'HOLX', 'HON', 'HOOD', 'HPK', 'HQY', 'HRMY', 'HSIC', 'HST', 'HTHT', 'HTZ', 'HUBG', 'HWC', 'HZNP', 'IAC', 'IART', 'IBKR', 'IBOC', 'IBRX', 'IBTX', 'ICLR', 'ICUI', 'IDXX', 'IEP', 'ILMN', 'IMCR', 'INCY', 'INDB', 'INMD', 'INSM', 'INTC', 'INTU', 'IONS', 'IOSP', 'IPAR', 'IPGP', 'IQ', 'IRDM', 'IRTC', 'ISEE', 'ISRG', 'ITCI', 'ITRI', 'JAMF', 'JAZZ', 'JBHT', 'JBLU', 'JD', 'JJSF', 'JKHY', 'KDP', 'KHC', 'KLAC', 'KLIC', 'KNBE', 'KRTX', 'LAMR', 'LANC', 'LAZR', 'LBRDA', 'LBRDK', 'LBTYA', 'LBTYB', 'LBTYK', 'LCID', 'LECO', 'LEGN', 'LESL', 'LFUS', 'LGIH', 'LHCG', 'LI', 'LITE', 'LIVN', 'LKQ', 'LNT', 'LNTH', 'LNW', 'LOGI', 'LOPE', 'LPLA', 'LRCX', 'LSCC', 'LSTR', 'LSXMA', 'LSXMB', 'LSXMK', 'LULU', 'LYFT', 'MANH', 'MAR', 'MASI', 'MAT', 'MBLY', 'MCHP', 'MDB', 'MDLZ', 'MDRX', 'MEDP', 'MELI', 'MEOH', 'META', 'MGEE', 'MGPI', 'MGRC', 'MIDD', 'MKSI', 'MKTX', 'MLCO', 'MMSI', 'MMYT', 'MNDY', 'MNST', 'MORN', 'MPWR', 'MQ', 'MRCY', 'MRNA', 'MRTX', 'MRVL', 'MSFT', 'MSTR', 'MTCH', 'MTSI', 'MU', 'MXL', 'NARI', 'NATI', 'NAVI', 'NBIX', 'NCNO', 'NDAQ', 'NDSN', 'NEOG', 'NFE', 'NFLX', 'NICE', 'NOVT', 'NSIT', 'NTAP', 'NTCT', 'NTES', 'NTLA', 'NTNX', 'NTRA', 'NTRS', 'NUVA', 'NVCR', 'NVDA', 'NVEE', 'NVEI', 'NVMI', 'NWE', 'NWL', 'NWS', 'NWSA', 'NWTN', 'NXPI', 'NXST', 'ODFL', 'ODP', 'OKTA', 'OLED', 'OLK', 'OLLI', 'OLPX', 'OMAB', 'OMCL', 'ON', 'ONB', 'ONEM', 'OPCH', 'ORLY', 'OTEX', 'OTTR', 'OZK', 'PAA', 'PAAS', 'PACB', 'PACW', 'PAGP', 'PANW', 'PARA', 'PARAA', 'PAYX', 'PCAR', 'PCH', 'PCTY', 'PCVX', 'PDCE', 'PDCO', 'PDD', 'PECO', 'PEGA', 'PENN', 'PEP', 'PFG', 'PGNY', 'PI', 'PINC', 'PLTK', 'PLUG', 'PLXS', 'PNFP', 'PODD', 'POOL', 'POWI', 'PPBI', 'PPC', 'PRFT', 'PRGS', 'PROK', 'PRTA', 'PRVA', 'PSEC', 'PSMT', 'PSNY', 'PSNYW', 'PTC', 'PTCT', 'PTEN', 'PTON', 'PTVE', 'PYCR', 'PYPL', 'PZZA', 'QCOM', 'QDEL', 'QFIN', 'QLYS', 'QRTEB', 'QRVO', 'RARE', 'RCM', 'REG', 'REGN', 'REYN', 'RGEN', 'RGLD', 'RIVN', 'RLAY', 'RMBS', 'RNST', 'RNW', 'ROIV', 'ROKU', 'ROST', 'RPD', 'RPRX', 'RRR', 'RUM', 'RUN', 'RUSHA', 'RUSHB', 'RVMD', 'RXDX', 'RYAAY', 'SABR', 'SAGE', 'SAIA', 'SANM', 'SBAC', 'SBLK', 'SBNY', 'SBRA', 'SBUX', 'SEDG', 'SEIC', 'SFM', 'SFNC', 'SGEN', 'SGML', 'SGRY', 'SHC', 'SHLS', 'SHOO', 'SIGI', 'SILK', 'SIMO', 'SIRI', 'SITM', 'SIVB', 'SLAB', 'SLM', 'SMCI', 'SMPL', 'SNPS', 'SNY', 'SOFI', 'SONO', 'SPLK', 'SPSC', 'SPT', 'SPWR', 'SRAD', 'SRCL', 'SRPT', 'SSB', 'SSNC', 'SSRM', 'STAA', 'STLD', 'STNE', 'STX', 'SWAV', 'SWKS', 'SYBT', 'SYNA', 'SYNH', 'TCBI', 'TCOM', 'TEAM', 'TECH', 'TENB', 'TER', 'TFSL', 'THRM', 'TIGO', 'TMUS', 'TNDM', 'TOWN', 'TPG', 'TRIP', 'TRMB', 'TRMD', 'TRMK', 'TROW', 'TRUP', 'TSCO', 'TSEM', 'TSLA', 'TTD', 'TTEC', 'TTEK', 'TTWO', 'TW', 'TWKS', 'TWNK', 'TXG', 'TXN', 'TXRH', 'UAL', 'UBSI', 'UCBI', 'UFPI', 'UHAL', 'UHALB', 'ULCC', 'ULTA', 'UMBF', 'UMPQ', 'URBN', 'UTHR', 'VC', 'VCYT', 'VERX', 'VIAV', 'VICR', 'VIR', 'VIRT', 'VLY', 'VNOM', 'VOD', 'VRNS', 'VRNT', 'VRRM', 'VRSK', 'VRSN', 'VRTX', 'VSAT', 'VTRS', 'WAFD', 'WB', 'WBA', 'WBD', 'WDAY', 'WDC', 'WDFC', 'WEN', 'WERN', 'WFRD', 'WING', 'WIRE', 'WIX', 'WMG', 'WOOF', 'WSBC', 'WSC', 'WSFS', 'WTFC', 'WTW', 'WWD', 'WYNN', 'XEL', 'XENE', 'XM', 'XP', 'XRAY', 'XRX', 'YY', 'Z', 'ZBRA', 'ZD', 'ZG', 'ZI', 'ZION', 'ZLAB', 'ZM', 'ZS']


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
@app.route('/index')
def main():
    """
    Function to handle all requests relating to the main page.
    This involves handling both the stock analyser form and the stock purchase form and related functionalities.
    """

    # variable to handle any error messages that come from purchase_form
    error_message = ""

    # sets default balance to $10,000
    if 'balance' not in session:
        session['balance'] = 10000

    # set default porfolio to include no stocks
    # session['stocks'] will be in the format {'stock name': no of stock}
    if 'stocks' not in session:
        session['stocks'] = {}

    # handles requests from purchase form (buying or selling stock)
    purchase_form = Buy_Sell_Stock()
    if purchase_form.validate_on_submit():
        form_data = request.form
        error_message = purchase_handler(form_data)

    # handles requests from stock analyser form
    form = Stock_Form()
    if form.validate_on_submit():
        form_data = request.form
        stock = form_data['Stock']
        script_cs, div_cs = candlestick_graph(stock)
        price = collect_stock_price(stock)
        try:
            return render_template('stock_after.html', script_cs=script_cs, div_cs=div_cs, stock_price=price,
                                   stock_name=stock.upper(), balance=str(session['balance']), error=error_message,
                                   purchase_form=purchase_form, stock_portfolio=session['stocks'])
        except:
            return render_template('stock_error.html')

    return render_template('stock_before.html', form=form, purchase_form=purchase_form, balance=str(session['balance']),
                           error=error_message, stock_portfolio=session['stocks'])


@app.errorhandler(404)
def page_not_found(e):
    """Handler in the case where user decides to enter unknown url"""

    return render_template('404.html')


def purchase_handler(form_data):
    """
    Purchase form handler
    Helps update stock portfolio and balance for the buy/sell requests
    """

    error_message = ""
    buy_sell = form_data['buy_sell']
    stock = form_data['stock'].upper()
    no_of_stocks = float(form_data['number_of_stocks'])

    if stock not in all_stocks:
        error_message = "Wrong Stock Name"
    else:
        price = float(collect_stock_price(form_data['stock']))
        if buy_sell == 'Buy' and session['balance'] < price * no_of_stocks:
            error_message = "Insufficient Balance in Account"
        elif (buy_sell == 'Sell' and stock not in session['stocks'].keys()) or (
                buy_sell == 'Sell' and stock in session['stocks'].keys() and session['stocks'][
            stock] < no_of_stocks):
            error_message = "Insufficient quantity of stock in account"
        elif buy_sell == 'Buy':
            session['balance'] -= price * no_of_stocks
            session['stocks'][stock] = session['stocks'].get(stock, 0) + no_of_stocks
        elif buy_sell == 'Sell':
            session['balance'] += price * no_of_stocks
            session['stocks'][stock] = session['stocks'].get(stock) - no_of_stocks
        else:
            raise ValueError

    return error_message


