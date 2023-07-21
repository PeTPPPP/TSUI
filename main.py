from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()

    parser.add_option("-x", dest="x", action="store_true", help="extracting TSUI")

    (options, args) = parser.parse_args()

    if options.x:
        from tsui_exporter.fisher_stats import runFisherAll
        runFisherAll()

