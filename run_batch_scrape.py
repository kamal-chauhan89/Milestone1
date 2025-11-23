"""
Quick Start Script for Batch Scraping
Run this script to start scraping all schemes from your document
"""

from batch_scraper import BatchMutualFundScraper
import sys

def main():
    print("=" * 60)
    print("GROWW MUTUAL FUND BATCH SCRAPER")
    print("=" * 60)
    
    # Update this path to your document
    doc_path = r"D:\download\Groww links for mutual funds.docx"
    
    # Check if custom path provided
    if len(sys.argv) > 1:
        doc_path = sys.argv[1]
    
    print(f"\nDocument path: {doc_path}")
    
    try:
        # Initialize batch scraper
        batch_scraper = BatchMutualFundScraper(delay_between_requests=2.0)
        
        # Step 1: Extract links from document
        print("\n" + "=" * 60)
        print("STEP 1: Extracting links from document...")
        print("=" * 60)
        
        links_data = batch_scraper.load_links_from_document(doc_path)
        
        # Save extracted links
        batch_scraper.parser.save_extracted_links(
            links_data, 
            'groww_all_scheme_links.json'
        )
        
        print(f"\n✅ Extracted {len(links_data['all_schemes'])} scheme URLs")
        
        if links_data.get('organized_by_amc'):
            print(f"✅ Found {len(links_data['organized_by_amc'])} AMCs")
            print("\nAMCs and scheme counts:")
            for amc, schemes in list(links_data['organized_by_amc'].items())[:10]:
                print(f"  • {amc}: {len(schemes)} schemes")
            if len(links_data['organized_by_amc']) > 10:
                print(f"  ... and {len(links_data['organized_by_amc']) - 10} more AMCs")
        
        # Step 2: Ask user what to scrape
        print("\n" + "=" * 60)
        print("STEP 2: Choose scraping option")
        print("=" * 60)
        print("\nOptions:")
        print("  1. Scrape ALL schemes (full scraping)")
        print("  2. Scrape by AMC (organized, saves progress per AMC)")
        print("  3. Scrape specific AMC")
        print("  4. Test with first 10 schemes")
        print("  5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n⚠️  This will scrape ALL schemes. This may take a long time.")
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm == 'yes':
                print("\nStarting full scraping...")
                batch_scraper.scrape_urls(links_data['all_schemes'])
            else:
                print("Cancelled.")
                return
        
        elif choice == "2":
            print("\nStarting organized scraping by AMC...")
            batch_scraper.scrape_by_amc(links_data)
        
        elif choice == "3":
            organized = links_data.get('organized_by_amc', {})
            if organized:
                print("\nAvailable AMCs:")
                amc_list = list(organized.keys())
                for i, amc in enumerate(amc_list, 1):
                    print(f"  {i}. {amc} ({len(organized[amc])} schemes)")
                
                try:
                    amc_idx = int(input("\nEnter AMC number: ").strip()) - 1
                    if 0 <= amc_idx < len(amc_list):
                        amc_name = amc_list[amc_idx]
                        print(f"\nScraping: {amc_name}")
                        batch_scraper.scrape_by_amc(links_data, amc_name)
                    else:
                        print("Invalid number")
                except ValueError:
                    print("Invalid input")
            else:
                print("No AMC organization found in document")
        
        elif choice == "4":
            print("\nTesting with first 10 schemes...")
            batch_scraper.scrape_urls(links_data['all_schemes'], max_urls=10)
        
        elif choice == "5":
            print("Exiting...")
            return
        
        else:
            print("Invalid choice")
            return
        
        # Step 3: Save results
        print("\n" + "=" * 60)
        print("STEP 3: Saving results...")
        print("=" * 60)
        
        batch_scraper.save_progress()
        batch_scraper.print_summary()
        
        print("\n✅ Scraping complete!")
        print(f"📁 Check the output JSON file for scraped data")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: File not found")
        print(f"   {e}")
        print(f"\nPlease update the document path in the script:")
        print(f"   doc_path = r\"D:\\download\\Groww links for mutual funds.docx\"")
    except ImportError as e:
        print(f"\n❌ Error: Missing dependency")
        print(f"   {e}")
        print(f"\nPlease install: pip install python-docx")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

