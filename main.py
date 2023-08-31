from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-x", dest="x", action="store_true", help="extracting TSUI")
    parser.add_option("-e", dest="e", action="store_true", help="encoding TSUI")

    (options, args) = parser.parse_args()

    if options.x:
        from tsui_sigtest_extractor.fisher_stats import runFisherAll
        runFisherAll()
    elif options.e:
        from tsui_encoding.tsui_encoding import run
        run()

