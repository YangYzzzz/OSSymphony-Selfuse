"""
Initial Setup: Create 5 ODT subdocument files for a legal brief
Task ID: writer_rm_074
Domain: libreoffice_writer
"""

import os
import shlex
import subprocess
import time
import zipfile
import io

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_074'

def launch_gui(command: str, delay_sec: float = 1.0):
    """Launch GUI app on VM display without blocking script exit."""
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )
    time.sleep(delay_sec)


def create_odt(filepath, content_xml_body):
    """Create a minimal ODT file with the given body content XML."""
    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"
                   manifest:version="1.2">
  <manifest:file-entry manifest:full-path="/" manifest:version="1.2"
                       manifest:media-type="application/vnd.oasis.opendocument.text"/>
  <manifest:file-entry manifest:full-path="content.xml"
                       manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="styles.xml"
                       manifest:media-type="text/xml"/>
  <manifest:file-entry manifest:full-path="meta.xml"
                       manifest:media-type="text/xml"/>
</manifest:manifest>'''

    content_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:automatic-styles>
    <style:style style:name="P_Title" style:family="paragraph">
      <style:paragraph-properties fo:text-align="center" fo:margin-bottom="0.3in"/>
      <style:text-properties fo:font-size="18pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="P_Heading" style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0.2in" fo:margin-bottom="0.1in"/>
      <style:text-properties fo:font-size="14pt" fo:font-weight="bold"/>
    </style:style>
    <style:style style:name="P_Body" style:family="paragraph">
      <style:paragraph-properties fo:margin-bottom="0.08in" fo:text-indent="0.5in"/>
      <style:text-properties fo:font-size="12pt"/>
    </style:style>
    <style:style style:name="P_BodyNoIndent" style:family="paragraph">
      <style:paragraph-properties fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt"/>
    </style:style>
  </office:automatic-styles>
  <office:body>
    <office:text>
{content_xml_body}
    </office:text>
  </office:body>
</office:document-content>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-styles
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"
    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
    office:version="1.2">
  <office:styles>
    <style:default-style style:family="paragraph">
      <style:paragraph-properties fo:margin-top="0in" fo:margin-bottom="0.08in"/>
      <style:text-properties fo:font-size="12pt" style:font-name="Liberation Serif"/>
    </style:default-style>
  </office:styles>
</office:document-styles>'''

    meta_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
    office:version="1.2">
  <office:meta/>
</office:document-meta>'''

    mimetype = 'application/vnd.oasis.opendocument.text'

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first entry, stored (not compressed)
        zf.writestr(zipfile.ZipInfo('mimetype', date_time=(2025, 1, 1, 0, 0, 0)), mimetype, compress_type=zipfile.ZIP_STORED)
        zf.writestr('META-INF/manifest.xml', manifest_xml)
        zf.writestr('content.xml', content_xml)
        zf.writestr('styles.xml', styles_xml)
        zf.writestr('meta.xml', meta_xml)

    with open(filepath, 'wb') as f:
        f.write(buf.getvalue())
    print(f'Created: {filepath}')


def create_initial():
    # --- Cover_Page.odt ---
    cover_body = '''      <text:p text:style-name="P_Title">IN THE UNITED STATES DISTRICT COURT</text:p>
      <text:p text:style-name="P_Title">FOR THE SOUTHERN DISTRICT OF NEW YORK</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Title">MERIDIAN TECHNOLOGIES, INC.,</text:p>
      <text:p text:style-name="P_Title">Plaintiff,</text:p>
      <text:p text:style-name="P_Title">v.</text:p>
      <text:p text:style-name="P_Title">ATLAS GLOBAL HOLDINGS, LLC,</text:p>
      <text:p text:style-name="P_Title">Defendant.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Title">Case No. 2025-CV-04821</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Title">PLAINTIFF'S MEMORANDUM OF LAW</text:p>
      <text:p text:style-name="P_Title">IN SUPPORT OF MOTION FOR SUMMARY JUDGMENT</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Submitted by:</text:p>
      <text:p text:style-name="P_BodyNoIndent">Katherine L. Morrison, Esq.</text:p>
      <text:p text:style-name="P_BodyNoIndent">Morrison &amp; Whitfield LLP</text:p>
      <text:p text:style-name="P_BodyNoIndent">350 Park Avenue, Suite 2200</text:p>
      <text:p text:style-name="P_BodyNoIndent">New York, NY 10022</text:p>
      <text:p text:style-name="P_BodyNoIndent">Tel: (212) 555-0142</text:p>
      <text:p text:style-name="P_BodyNoIndent">Email: kmorrison@morrisonwhitfield.com</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Dated: March 15, 2025</text:p>'''
    create_odt(f'{WORKDIR}/Cover_Page.odt', cover_body)

    # --- Table_of_Authorities.odt ---
    toa_body = '''      <text:p text:style-name="P_Title">TABLE OF AUTHORITIES</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">Cases</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Anderson v. Liberty Lobby, Inc., 477 U.S. 242 (1986) ......... 4, 7, 12</text:p>
      <text:p text:style-name="P_BodyNoIndent">Celotex Corp. v. Catrett, 477 U.S. 317 (1986) ......... 4, 8</text:p>
      <text:p text:style-name="P_BodyNoIndent">Matsushita Elec. Indus. Co. v. Zenith Radio Corp., 475 U.S. 574 (1986) ......... 5, 9</text:p>
      <text:p text:style-name="P_BodyNoIndent">Scott v. Harris, 550 U.S. 372 (2007) ......... 6</text:p>
      <text:p text:style-name="P_BodyNoIndent">Tolan v. Cotton, 572 U.S. 650 (2014) ......... 7</text:p>
      <text:p text:style-name="P_BodyNoIndent">Adickes v. S.H. Kress &amp; Co., 398 U.S. 144 (1970) ......... 8, 15</text:p>
      <text:p text:style-name="P_BodyNoIndent">Lujan v. Defenders of Wildlife, 504 U.S. 555 (1992) ......... 10</text:p>
      <text:p text:style-name="P_BodyNoIndent">Ashcroft v. Iqbal, 556 U.S. 662 (2009) ......... 11, 14</text:p>
      <text:p text:style-name="P_BodyNoIndent">Bell Atl. Corp. v. Twombly, 550 U.S. 544 (2007) ......... 11</text:p>
      <text:p text:style-name="P_BodyNoIndent">Reeves v. Sanderson Plumbing Prods., Inc., 530 U.S. 133 (2000) ......... 13</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">Statutes</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">15 U.S.C. Section 1 (Sherman Act) ......... 3, 6, 9</text:p>
      <text:p text:style-name="P_BodyNoIndent">15 U.S.C. Section 2 ......... 4, 10</text:p>
      <text:p text:style-name="P_BodyNoIndent">Fed. R. Civ. P. 56 ......... 4, 7</text:p>
      <text:p text:style-name="P_BodyNoIndent">28 U.S.C. Section 1331 ......... 3</text:p>
      <text:p text:style-name="P_BodyNoIndent">28 U.S.C. Section 1337 ......... 3</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">Other Authorities</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Areeda &amp; Hovenkamp, Antitrust Law (4th ed. 2023) ......... 9, 12</text:p>
      <text:p text:style-name="P_BodyNoIndent">Restatement (Third) of Unfair Competition Section 39 ......... 14</text:p>'''
    create_odt(f'{WORKDIR}/Table_of_Authorities.odt', toa_body)

    # --- Statement_of_Facts.odt (8 pages worth of content) ---
    sof_body = '''      <text:p text:style-name="P_Title">STATEMENT OF FACTS</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">I. Background of the Parties</text:p>
      <text:p text:style-name="P_Body">Plaintiff Meridian Technologies, Inc. ("Meridian") is a Delaware corporation with its principal place of business in New York, New York. Meridian was founded in 2008 by Dr. Elena Vasquez and has grown to become one of the leading providers of enterprise cloud infrastructure solutions in the United States, serving over 2,400 corporate clients across 38 states. Meridian's annual revenue for fiscal year 2024 was approximately $847 million, with a workforce of 3,200 employees.</text:p>
      <text:p text:style-name="P_Body">Defendant Atlas Global Holdings, LLC ("Atlas") is a multinational technology conglomerate incorporated in the State of Delaware and headquartered in San Francisco, California. Atlas operates through numerous subsidiaries and affiliated entities across 14 countries. Atlas reported consolidated revenue of $23.6 billion for fiscal year 2024 and maintains a dominant market position in several technology sectors, including cloud computing, data analytics, and enterprise software.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">II. The Relevant Market</text:p>
      <text:p text:style-name="P_Body">The relevant product market in this action is the market for enterprise cloud infrastructure services, which encompasses the provision of scalable computing resources, data storage solutions, and network infrastructure delivered via cloud-based platforms to business customers. This market is distinct from consumer cloud services, which serve individual end users for personal storage and application hosting.</text:p>
      <text:p text:style-name="P_Body">The relevant geographic market is the United States. Enterprise cloud infrastructure services require compliance with domestic data residency regulations, proximity to major internet exchange points, and relationships with domestic telecommunications providers. Cross-border substitution is limited due to regulatory constraints under federal procurement rules and data sovereignty requirements imposed by major institutional clients.</text:p>
      <text:p text:style-name="P_Body">According to industry analyst reports from Gartner and IDC, the U.S. enterprise cloud infrastructure market was valued at approximately $94.7 billion in 2024. Atlas held approximately 41% market share, while Meridian held approximately 8.3%. The next largest competitors were Pinnacle Systems (12.1%), Orion Cloud Corp. (9.7%), and Nextera Solutions (7.2%).</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">III. Atlas's Exclusionary Conduct</text:p>
      <text:p text:style-name="P_Body">Beginning in approximately January 2022, Atlas embarked on a systematic campaign to exclude Meridian and other competitors from the enterprise cloud infrastructure market through a series of anticompetitive practices. These practices included exclusive dealing arrangements, predatory pricing strategies, and deliberate interference with Meridian's business relationships.</text:p>
      <text:p text:style-name="P_Body">On or about January 15, 2022, Atlas introduced its "Preferred Partner Program," which offered significant volume discounts of up to 45% to enterprise customers who agreed to source at least 85% of their cloud infrastructure needs exclusively from Atlas. Internal Atlas documents obtained during discovery reveal that this program was specifically designed to "lock out mid-tier competitors like Meridian" and to "consolidate market share before regulatory scrutiny intensifies." (Ex. A, Internal Memorandum from David Chen, SVP of Strategy, to Atlas Board of Directors, dated December 3, 2021.)</text:p>
      <text:p text:style-name="P_Body">Between January 2022 and September 2024, Atlas enrolled 847 enterprise customers in the Preferred Partner Program, representing approximately $12.3 billion in annual cloud spending. Of these customers, 142 had previously maintained active service agreements with Meridian. Following their enrollment in the Preferred Partner Program, 128 of these 142 customers terminated or substantially reduced their contracts with Meridian, resulting in lost revenue of approximately $186 million over the relevant period.</text:p>
      <text:p text:style-name="P_Body">In addition to the exclusive dealing arrangements, Atlas engaged in predatory pricing in targeted geographic and customer segments where Meridian maintained its strongest market presence. Specifically, Atlas offered below-cost pricing to enterprise customers in the New York metropolitan area, the Chicago metropolitan area, and the Boston-Washington corridor, which collectively accounted for approximately 62% of Meridian's revenue base.</text:p>
      <text:p text:style-name="P_Body">Expert analysis conducted by Dr. Robert Thornton, an economist retained by Meridian, demonstrates that Atlas priced its services below average variable cost in these targeted regions during the period from March 2022 through December 2023. Dr. Thornton's analysis shows that Atlas's pricing in these regions was, on average, 23% below its average variable cost, resulting in estimated losses to Atlas of approximately $340 million. Dr. Thornton opines that this pricing strategy is consistent with predatory pricing designed to eliminate competition, with the expectation of recouping losses through supracompetitive pricing once competitors have been driven from the market. (Ex. B, Expert Report of Dr. Robert Thornton, dated February 1, 2025.)</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">IV. Interference with Business Relationships</text:p>
      <text:p text:style-name="P_Body">Atlas further engaged in tortious interference with Meridian's prospective business relationships. In at least seven documented instances between March 2022 and August 2024, Atlas representatives contacted Meridian's prospective clients during active contract negotiations and offered substantially discounted competing proposals, accompanied by disparaging statements about Meridian's financial stability and service reliability.</text:p>
      <text:p text:style-name="P_Body">For example, on June 14, 2023, during Meridian's final negotiations with Harborview Financial Group for a five-year, $34 million cloud migration contract, Atlas's Regional Vice President, James Calloway, contacted Harborview's Chief Technology Officer directly and stated that "Meridian is hemorrhaging clients and may not survive the next eighteen months" and that "committing to Meridian at this stage would be a significant business risk." (Ex. C, Deposition of Margaret Liu, CTO of Harborview Financial Group, at 47:12-48:3.) Mr. Calloway simultaneously offered Harborview a competing proposal at approximately 40% below Atlas's standard pricing for comparable services.</text:p>
      <text:p text:style-name="P_Body">As a direct result of Atlas's interference, Harborview terminated negotiations with Meridian and entered into a contract with Atlas. Similar interference occurred with respect to Meridian's negotiations with Crestline Manufacturing, Pacific Northwest Health Systems, Dominion Energy Solutions, Vanguard Aerospace Technologies, Sterling Capital Management, and Brightpath Education Consortium.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">V. Impact on Meridian</text:p>
      <text:p text:style-name="P_Body">The cumulative effect of Atlas's anticompetitive conduct has been devastating to Meridian's business operations and competitive position. Between fiscal year 2022 and fiscal year 2024, Meridian's market share declined from 11.4% to 8.3%, representing a loss of approximately $293 million in annual revenue. Meridian has been forced to reduce its workforce by approximately 480 employees, close two regional data centers, and defer planned investments in next-generation infrastructure totaling $125 million.</text:p>
      <text:p text:style-name="P_Body">Furthermore, Meridian's ability to compete for new business has been significantly impaired. Industry surveys conducted by Forrester Research indicate that enterprise decision-makers increasingly view Meridian as a "second-tier provider" and express concerns about Meridian's long-term viability, concerns that are directly traceable to Atlas's campaign of disparagement and market exclusion.</text:p>'''
    create_odt(f'{WORKDIR}/Statement_of_Facts.odt', sof_body)

    # --- Argument.odt (15 pages worth of legal argument) ---
    arg_body = '''      <text:p text:style-name="P_Title">ARGUMENT</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">I. STANDARD OF REVIEW</text:p>
      <text:p text:style-name="P_Body">Summary judgment is appropriate when "there is no genuine dispute as to any material fact and the movant is entitled to judgment as a matter of law." Fed. R. Civ. P. 56(a). The moving party bears the initial burden of demonstrating the absence of a genuine issue of material fact. Celotex Corp. v. Catrett, 477 U.S. 317, 323 (1986). Once this burden is met, the nonmoving party must come forward with "specific facts showing that there is a genuine issue for trial." Anderson v. Liberty Lobby, Inc., 477 U.S. 242, 248 (1986).</text:p>
      <text:p text:style-name="P_Body">In evaluating a motion for summary judgment, the court must view all evidence and draw all reasonable inferences in the light most favorable to the nonmoving party. Matsushita Elec. Indus. Co. v. Zenith Radio Corp., 475 U.S. 574, 587 (1986). However, the nonmoving party may not rest upon mere allegations or denials but must set forth specific facts demonstrating a genuine dispute. Scott v. Harris, 550 U.S. 372, 380 (2007). Where the record taken as a whole could not lead a rational trier of fact to find for the nonmoving party, summary judgment is warranted. Id.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">II. ATLAS VIOLATED SECTION 2 OF THE SHERMAN ACT THROUGH MONOPOLIZATION</text:p>
      <text:p text:style-name="P_Body">Section 2 of the Sherman Act, 15 U.S.C. Section 2, prohibits monopolization and attempts to monopolize any part of trade or commerce among the several states. To establish a claim of monopolization, a plaintiff must prove: (1) the possession of monopoly power in the relevant market; and (2) the willful acquisition or maintenance of that power through anticompetitive conduct, as distinguished from growth or development as a consequence of a superior product, business acumen, or historic accident. United States v. Grinnell Corp., 384 U.S. 563, 570-71 (1966).</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">A. Atlas Possesses Monopoly Power in the Relevant Market</text:p>
      <text:p text:style-name="P_Body">Monopoly power is the power to control prices or exclude competition in the relevant market. United States v. E.I. du Pont de Nemours &amp; Co., 351 U.S. 377, 391 (1956). While no single factor is determinative, courts regularly consider market share, barriers to entry, and the structure of the relevant market in assessing monopoly power.</text:p>
      <text:p text:style-name="P_Body">Atlas's 41% market share in the U.S. enterprise cloud infrastructure market, while not alone dispositive, is strong evidence of monopoly power when considered in conjunction with significant barriers to entry and Atlas's demonstrated ability to control pricing. Courts have found monopoly power at comparable or lower market share levels where, as here, other indicia of market power are present. See, e.g., Eastman Kodak Co. v. Image Technical Services, Inc., 504 U.S. 451 (1992) (finding sufficient evidence of monopoly power where defendant controlled approximately 80% of relevant market).</text:p>
      <text:p text:style-name="P_Body">The barriers to entry in the enterprise cloud infrastructure market are substantial and well-documented. New entrants must invest billions of dollars in physical data center infrastructure, obtain numerous regulatory approvals and security certifications, develop sophisticated software platforms, and establish relationships with enterprise procurement departments. Dr. Thornton estimates that a new entrant seeking to achieve minimum viable scale in this market would need to invest approximately $4.2 billion over a three- to five-year period. (Ex. B, Thornton Report at 34-38.)</text:p>
      <text:p text:style-name="P_Body">Furthermore, the market exhibits significant network effects and switching costs. Enterprise customers who have migrated their operations to a particular cloud platform face substantial costs in transitioning to an alternative provider, including data migration expenses, application reconfiguration, employee retraining, and operational disruption. These switching costs, which Dr. Thornton estimates average $2.3 million per enterprise customer, create a "lock-in" effect that reinforces the market position of incumbent providers and further deters new entry.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">B. Atlas Willfully Maintained Its Monopoly Power Through Anticompetitive Conduct</text:p>
      <text:p text:style-name="P_Body">The undisputed evidence demonstrates that Atlas engaged in at least three distinct categories of anticompetitive conduct to maintain and extend its monopoly power: (1) exclusive dealing arrangements that foreclosed a substantial share of the relevant market; (2) predatory pricing designed to eliminate competitors; and (3) tortious interference with competitors' business relationships.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">1. Exclusive Dealing Arrangements</text:p>
      <text:p text:style-name="P_Body">Exclusive dealing arrangements violate the antitrust laws when they foreclose a substantial share of the relevant market to competitors. Tampa Electric Co. v. Nashville Coal Co., 365 U.S. 320, 327 (1961). In assessing whether exclusive dealing arrangements are anticompetitive, courts consider the percentage of the relevant market foreclosed, the duration of the exclusivity provision, the likelihood of anticompetitive effects, and any procompetitive justifications. ZF Meritor, LLC v. Eaton Corp., 696 F.3d 254, 270 (3d Cir. 2012).</text:p>
      <text:p text:style-name="P_Body">Atlas's Preferred Partner Program foreclosed approximately 35% of the total enterprise cloud infrastructure market to competition. The program required participating customers to commit to sourcing at least 85% of their cloud needs from Atlas for a minimum term of three years. Courts have found foreclosure of substantially lower percentages to be anticompetitive. See, e.g., United States v. Microsoft Corp., 253 F.3d 34, 70 (D.C. Cir. 2001) (exclusive dealing agreements foreclosing substantially less than 40% of the market held anticompetitive).</text:p>
      <text:p text:style-name="P_Body">Moreover, the internal documents produced during discovery leave no doubt as to the anticompetitive intent behind the Preferred Partner Program. The December 2021 memorandum from David Chen explicitly stated that the program's objective was to "systematically foreclose the mid-market segment" and to "create insurmountable switching barriers for enrolled customers." (Ex. A at 3.) A follow-up strategy presentation from February 2022 projected that the program would "reduce competitors' addressable market by 30-40% within 24 months" and would "accelerate the exit of marginal competitors from the market." (Ex. D, Atlas Strategy Presentation, dated February 15, 2022, at Slide 14.)</text:p>
      <text:p text:style-name="P_Body">Atlas cannot offer any legitimate procompetitive justification for its exclusive dealing arrangements. While Atlas has suggested that the Preferred Partner Program provides "enhanced service levels" to participating customers, discovery has revealed that the service specifications for Preferred Partner customers are identical to those offered to non-exclusive customers at standard pricing. (Ex. E, Deposition of Sarah Martinez, Atlas VP of Customer Success, at 112:7-113:15.) The sole purpose and effect of the program was to lock customers into exclusive arrangements and foreclose competitors from competing for their business.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">2. Predatory Pricing</text:p>
      <text:p text:style-name="P_Body">Predatory pricing claims require proof that: (1) the defendant priced below an appropriate measure of cost; and (2) the defendant had a dangerous probability of recouping its investment in below-cost pricing. Brooke Group Ltd. v. Brown &amp; Williamson Tobacco Corp., 509 U.S. 209, 222-24 (1993). Both elements are satisfied here.</text:p>
      <text:p text:style-name="P_Body">As detailed in Section III of the Statement of Facts, Dr. Thornton's expert analysis conclusively demonstrates that Atlas priced its enterprise cloud infrastructure services below average variable cost in three key geographic regions over a 22-month period. Atlas's pricing was, on average, 23% below its average variable cost, and the total investment in below-cost pricing was approximately $340 million. This is not a case of temporary promotional pricing or competitive response; rather, it was a sustained, targeted campaign to destroy Meridian's competitive position in its core markets.</text:p>
      <text:p text:style-name="P_Body">The dangerous probability of recoupment is established by the structure of the market. As discussed above, the enterprise cloud infrastructure market is characterized by high barriers to entry, significant switching costs, and network effects. Once competitors are eliminated from a geographic region, customers face substantial costs in switching to alternative providers, enabling the dominant firm to raise prices to supracompetitive levels. Dr. Thornton's economic modeling projects that Atlas would recoup its $340 million investment in predatory pricing within approximately 30 months of achieving market dominance in the targeted regions, through price increases averaging 18% above pre-predation levels. (Ex. B, Thornton Report at 56-62.)</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">3. Tortious Interference</text:p>
      <text:p text:style-name="P_Body">Atlas's systematic interference with Meridian's prospective business relationships constitutes independently actionable anticompetitive conduct. Under New York law, tortious interference with prospective business relations requires: (1) the plaintiff had business relations with a third party; (2) the defendant interfered with those business relations; (3) the defendant acted for a wrongful purpose or used dishonest, unfair, or improper means; and (4) the defendant's conduct caused injury to the plaintiff's business relationship. Carvel Corp. v. Noonan, 3 N.Y.3d 182, 189 (2004).</text:p>
      <text:p text:style-name="P_Body">Each of these elements is satisfied with respect to the seven documented instances of Atlas's interference described in the Statement of Facts. In each instance, Meridian was engaged in active, advanced-stage contract negotiations with prospective clients. Atlas's representatives affirmatively intervened in these negotiations through direct communications with the prospective clients' decision-makers, offering below-market pricing combined with false and disparaging statements about Meridian's financial condition and service capabilities. As a direct result, each prospective client terminated negotiations with Meridian and entered into contracts with Atlas.</text:p>
      <text:p text:style-name="P_Body">The use of false statements to disparage a competitor constitutes "improper means" under New York tortious interference law. Guard-Life Corp. v. S. Parker Hardware Mfg. Corp., 50 N.Y.2d 183, 191 (1980). Mr. Calloway's statement that "Meridian is hemorrhaging clients and may not survive the next eighteen months" was demonstrably false at the time it was made. Meridian's financial statements for the quarter ending June 30, 2023 showed revenue of $198 million, positive operating cash flow of $23 million, and cash reserves of $142 million. (Ex. F, Meridian Technologies Q2 2023 Financial Statements.) Far from being on the verge of collapse, Meridian was a profitable, cash-generating enterprise that was fully capable of performing under the proposed Harborview contract.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">III. ATLAS'S CONDUCT ALSO CONSTITUTES A CONSPIRACY TO RESTRAIN TRADE UNDER SECTION 1 OF THE SHERMAN ACT</text:p>
      <text:p text:style-name="P_Body">In addition to monopolization under Section 2, Atlas's exclusive dealing program constitutes an unreasonable restraint of trade in violation of Section 1 of the Sherman Act, 15 U.S.C. Section 1. Section 1 prohibits "every contract, combination in the form of trust or otherwise, or conspiracy, in restraint of trade." The Preferred Partner Program agreements between Atlas and its enrolled customers constitute "contracts" that unreasonably restrain trade in the enterprise cloud infrastructure market.</text:p>
      <text:p text:style-name="P_Body">Under the rule of reason analysis applicable to exclusive dealing claims under Section 1, courts weigh the anticompetitive effects of the restraint against any procompetitive justifications. As demonstrated above, the Preferred Partner Program forecloses approximately 35% of the relevant market, and Atlas has failed to offer any legitimate procompetitive justification. The anticompetitive effects substantially outweigh any purported benefits, and the restraint is therefore unreasonable as a matter of law.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Heading">IV. MERIDIAN HAS SUFFERED ANTITRUST INJURY AND IS ENTITLED TO DAMAGES</text:p>
      <text:p text:style-name="P_Body">Section 4 of the Clayton Act, 15 U.S.C. Section 15, provides that "any person who shall be injured in his business or property by reason of anything forbidden in the antitrust laws" may recover treble damages. Meridian has suffered antitrust injury flowing directly from Atlas's anticompetitive conduct.</text:p>
      <text:p text:style-name="P_Body">Meridian's damages include: (1) lost revenue from the 128 customers who terminated or reduced their contracts following enrollment in the Preferred Partner Program ($186 million); (2) lost revenue from the seven prospective clients with whom Atlas tortiously interfered ($87 million in projected contract value); (3) lost profits attributable to predatory pricing in Meridian's core geographic markets ($124 million); and (4) diminished enterprise value resulting from Atlas's campaign of disparagement and market exclusion ($340 million, based on the analysis of Dr. Angela Reeves, Meridian's damages expert). (Ex. G, Expert Report of Dr. Angela Reeves, dated February 8, 2025.)</text:p>
      <text:p text:style-name="P_Body">Meridian's total actual damages are estimated at $737 million. Under Section 4 of the Clayton Act, Meridian is entitled to treble damages of $2.211 billion, plus reasonable attorneys' fees and costs of suit.</text:p>'''
    create_odt(f'{WORKDIR}/Argument.odt', arg_body)

    # --- Conclusion.odt ---
    conc_body = '''      <text:p text:style-name="P_Title">CONCLUSION</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_Body">For the foregoing reasons, Plaintiff Meridian Technologies, Inc. respectfully requests that this Court grant its motion for summary judgment on all claims against Defendant Atlas Global Holdings, LLC. The undisputed material facts demonstrate that Atlas engaged in a systematic campaign of anticompetitive conduct, including exclusive dealing arrangements, predatory pricing, and tortious interference with Meridian's business relationships, in willful violation of Sections 1 and 2 of the Sherman Act.</text:p>
      <text:p text:style-name="P_Body">The evidence establishes beyond genuine dispute that Atlas possessed monopoly power in the U.S. enterprise cloud infrastructure market and willfully maintained that power through conduct that had no legitimate business justification. Atlas's anticompetitive practices directly caused Meridian to suffer substantial damages, including lost revenue, lost profits, and diminished enterprise value totaling approximately $737 million.</text:p>
      <text:p text:style-name="P_Body">Meridian therefore respectfully requests that this Court enter judgment in its favor and award treble damages in the amount of $2.211 billion pursuant to Section 4 of the Clayton Act, 15 U.S.C. Section 15, together with reasonable attorneys' fees and costs of suit, and such other and further relief as this Court deems just and appropriate.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Respectfully submitted,</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">_______________________________</text:p>
      <text:p text:style-name="P_BodyNoIndent">Katherine L. Morrison, Esq.</text:p>
      <text:p text:style-name="P_BodyNoIndent">Morrison &amp; Whitfield LLP</text:p>
      <text:p text:style-name="P_BodyNoIndent">350 Park Avenue, Suite 2200</text:p>
      <text:p text:style-name="P_BodyNoIndent">New York, NY 10022</text:p>
      <text:p text:style-name="P_BodyNoIndent">Tel: (212) 555-0142</text:p>
      <text:p text:style-name="P_BodyNoIndent">Email: kmorrison@morrisonwhitfield.com</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Attorneys for Plaintiff</text:p>
      <text:p text:style-name="P_BodyNoIndent">Meridian Technologies, Inc.</text:p>
      <text:p text:style-name="P_BodyNoIndent"> </text:p>
      <text:p text:style-name="P_BodyNoIndent">Dated: March 15, 2025</text:p>'''
    create_odt(f'{WORKDIR}/Conclusion.odt', conc_body)

    # Open file manager to show the files, and open one ODT to have Writer ready
    launch_gui(f'nautilus "{WORKDIR}"', delay_sec=2.0)
    launch_gui(f'libreoffice --writer "{WORKDIR}/Cover_Page.odt"', delay_sec=3.0)
    print('GUI_READY: launched Nautilus file manager and LibreOffice Writer with DISPLAY=:0')


create_initial()
