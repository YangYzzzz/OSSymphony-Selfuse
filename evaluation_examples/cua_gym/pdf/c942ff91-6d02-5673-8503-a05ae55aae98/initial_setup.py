"""
Initial Setup: Create a 30-page legal brief PDF for text extraction task
Task ID: pdf_legal_089
Domain: pdf
"""

import os
import shlex
import subprocess
import time
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_089'
BRIEF_DIR = f'{WORKDIR}/legal/opposing'
OUTPUT = f'{BRIEF_DIR}/brief.pdf'

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

# Legal brief content sections - realistic opposing counsel brief
BRIEF_SECTIONS = [
    # Section 0: Cover page
    {
        "title": "",
        "content": """IN THE UNITED STATES DISTRICT COURT
FOR THE SOUTHERN DISTRICT OF NEW YORK

Case No. 2025-CV-04382

MERIDIAN HEALTHCARE SYSTEMS, INC.,
Plaintiff,

v.

PINNACLE PHARMACEUTICALS CORP.,
Defendant.

DEFENDANT'S MEMORANDUM OF LAW
IN OPPOSITION TO PLAINTIFF'S
MOTION FOR PRELIMINARY INJUNCTION

Submitted by:
BLACKSTONE & WHITFIELD LLP
1200 Avenue of the Americas, 38th Floor
New York, NY 10036

Katherine M. Harrington, Esq.
Daniel R. Ostrowski, Esq.
Counsel for Defendant

Date: March 15, 2025"""
    },
    # Section 1: Table of Contents
    {
        "title": "TABLE OF CONTENTS",
        "content": """TABLE OF AUTHORITIES . . . . . . . . . . . . . . . . . . . . . . . . . . . . ii

PRELIMINARY STATEMENT . . . . . . . . . . . . . . . . . . . . . . . . . . 1

STATEMENT OF FACTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3

ARGUMENT . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8

I.  PLAINTIFF CANNOT DEMONSTRATE A LIKELIHOOD
    OF SUCCESS ON THE MERITS . . . . . . . . . . . . . . . . . . . 8

    A. The Patent Claims Are Invalid Under 35 U.S.C. 103 . . . . 9
    B. Defendant's Product Does Not Infringe . . . . . . . . . . . . 14
    C. Prosecution History Estoppel Bars Plaintiff's Claims . . . . 18

II. PLAINTIFF CANNOT SHOW IRREPARABLE HARM . . . . . . . 20

III. THE BALANCE OF EQUITIES FAVORS DEFENDANT . . . . . . 23

IV. THE PUBLIC INTEREST WEIGHS AGAINST INJUNCTION . . . 25

CONCLUSION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28"""
    },
    # Section 2: Table of Authorities
    {
        "title": "TABLE OF AUTHORITIES",
        "content": """CASES

Abbott Laboratories v. Sandoz, Inc., 566 F.3d 1282 (Fed. Cir. 2009) . . . . . 12, 15

Amazon.com, Inc. v. Barnesandnoble.com, Inc., 239 F.3d 1343
(Fed. Cir. 2001) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9, 21

eBay Inc. v. MercExchange, L.L.C., 547 U.S. 388 (2006) . . . . . . . . . 8, 20, 23

Graham v. John Deere Co., 383 U.S. 1 (1966) . . . . . . . . . . . . . . . . . 10

KSR International Co. v. Teleflex Inc., 550 U.S. 398 (2007) . . . . . . 10, 11, 13

Markman v. Westview Instruments, Inc., 517 U.S. 370 (1996) . . . . . . . . 14

Phillips v. AWH Corp., 415 F.3d 1303 (Fed. Cir. 2005) . . . . . . . . . . . 14, 15

Winter v. Natural Resources Defense Council, Inc.,
555 U.S. 7 (2008) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8, 20

STATUTES

35 U.S.C. Section 102 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
35 U.S.C. Section 103 . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9, 10, 13
35 U.S.C. Section 112 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
35 U.S.C. Section 271 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

OTHER AUTHORITIES

Federal Rules of Civil Procedure, Rule 65 . . . . . . . . . . . . . . . . . . 8
Manual of Patent Examining Procedure Section 2143 . . . . . . . . . . . . 11"""
    },
    # Section 3: Preliminary Statement
    {
        "title": "PRELIMINARY STATEMENT",
        "content": """Defendant Pinnacle Pharmaceuticals Corp. respectfully submits this memorandum of law in opposition to Plaintiff Meridian Healthcare Systems, Inc.'s motion for a preliminary injunction. The preliminary injunction sought by Plaintiff would effectively remove from the market Defendant's cardiovascular therapeutic compound, Cardiovan, which has been prescribed to thousands of patients suffering from chronic atrial fibrillation and related cardiovascular conditions.

Plaintiff's motion should be denied for several independent reasons. First, Plaintiff cannot demonstrate a likelihood of success on the merits because the asserted patent claims are invalid as obvious under 35 U.S.C. Section 103. The prior art references, including the Nakamura publication and the European Patent Application filed by Bergstrom, disclose every limitation of the claimed invention. The combination of these references would have been obvious to a person of ordinary skill in the pharmaceutical arts at the time of the alleged invention.

Second, even if the patent were valid, Defendant's Cardiovan product does not infringe the asserted claims. The active pharmaceutical ingredient in Cardiovan utilizes a fundamentally different molecular mechanism than the compound described in the patent claims. Plaintiff's infringement theory relies on an impermissibly broad construction of the claim term "therapeutically effective amount" that is inconsistent with the intrinsic evidence and the prosecution history.

Third, Plaintiff cannot demonstrate irreparable harm because it has unreasonably delayed in seeking injunctive relief. Plaintiff was aware of Defendant's product launch more than fourteen months before filing this motion. Courts have consistently held that such delays undermine claims of irreparable injury. Moreover, Plaintiff's harm, if any, is fully compensable through monetary damages.

Finally, the balance of equities and the public interest weigh heavily against injunctive relief. Removing Cardiovan from the market would deprive thousands of patients of a critical medication that has demonstrated superior efficacy and tolerability compared to existing alternatives. The public interest in continued access to life-saving pharmaceuticals far outweighs Plaintiff's speculative claims of market share erosion."""
    },
    # Section 4: Statement of Facts (Part 1)
    {
        "title": "STATEMENT OF FACTS",
        "content": """A. The Parties and Their Products

Plaintiff Meridian Healthcare Systems, Inc. is a Delaware corporation with its principal place of business in Princeton, New Jersey. Meridian manufactures and distributes pharmaceutical products, including its cardiovascular drug Rhythmex, which received FDA approval in 2019 for the treatment of persistent atrial fibrillation. Declaration of Katherine M. Harrington, Exhibit A.

Defendant Pinnacle Pharmaceuticals Corp. is a Maryland corporation headquartered in Baltimore, Maryland. Pinnacle is a specialty pharmaceutical company focused on developing novel therapeutic compounds for cardiovascular and metabolic disorders. Pinnacle received FDA approval for Cardiovan on September 12, 2024, following completion of extensive Phase III clinical trials demonstrating the drug's safety and efficacy. Harrington Decl., Exhibit B.

B. The Patent at Issue

Plaintiff asserts U.S. Patent No. 10,847,293 (the "'293 Patent"), titled "Compositions and Methods for Treating Cardiac Arrhythmia Using Modified Benzofuran Derivatives." The '293 Patent was filed on June 3, 2017, and issued on November 24, 2020. The patent describes pharmaceutical compositions containing certain benzofuran derivative compounds that allegedly demonstrate anti-arrhythmic properties through modulation of cardiac ion channel activity.

The '293 Patent contains twenty-three claims, of which claims 1, 7, 12, and 18 are asserted against Defendant. Claim 1, the only independent claim at issue, recites:

A pharmaceutical composition comprising a therapeutically effective amount of a compound having the structural formula described in Formula I, or a pharmaceutically acceptable salt thereof, and a pharmaceutically acceptable carrier, wherein said composition is formulated for oral administration and provides a sustained plasma concentration of said compound over a period of at least twelve hours.

The specification describes the compound of Formula I as a 2,3-disubstituted benzofuran derivative with specific functional groups at the C-5 and C-7 positions that are said to facilitate selective binding to hERG potassium channels without producing the cardiotoxic effects associated with prior art compounds."""
    },
    # Section 5: Statement of Facts (Part 2)
    {
        "title": "",
        "content": """C. The Prior Art

The prior art landscape in the field of anti-arrhythmic benzofuran derivatives was well-developed at the time of the alleged invention. The following references are particularly relevant:

1. Nakamura et al., "Synthesis and Pharmacological Evaluation of Novel Benzofuran-Based Ion Channel Modulators," Journal of Medicinal Chemistry, Vol. 58, pp. 4712-4728 (2015) ("Nakamura"). This reference discloses a series of 2,3-disubstituted benzofuran compounds with anti-arrhythmic activity, including compounds with substitutions at the C-5 position that are structurally analogous to the claimed Formula I. Nakamura reports that these compounds selectively modulate hERG potassium channel conductance with IC50 values ranging from 0.3 to 2.4 micromolar. Harrington Decl., Exhibit D.

2. European Patent Application No. EP 2,847,103 A1 to Bergstrom et al. ("Bergstrom"). Published on March 18, 2015, this application describes oral pharmaceutical formulations of benzofuran derivatives designed to achieve sustained-release pharmacokinetic profiles. Bergstrom specifically teaches the use of hydroxypropyl methylcellulose matrices to achieve twelve-hour sustained plasma concentrations of benzofuran-based active pharmaceutical ingredients. Harrington Decl., Exhibit E.

3. Chen et al., "Structure-Activity Relationships of Benzofuran Derivatives as Cardiac Ion Channel Modulators," Bioorganic & Medicinal Chemistry Letters, Vol. 24, pp. 1891-1896 (2014) ("Chen"). This reference identifies the C-7 position of the benzofuran ring as critical for selectivity between cardiac ion channel subtypes and discloses several C-7 substituted analogs with favorable therapeutic indices. Harrington Decl., Exhibit F.

D. Defendant's Product Development

Pinnacle initiated its Cardiovan research program in 2016, well before the filing date of the '293 Patent. The research team, led by Dr. Samantha Reeves, developed Cardiovan through an independent research pathway that focused on a distinct class of benzofuran-based compounds. The Cardiovan active ingredient, designated PPC-4892, employs a novel C-4 amide linkage that is not found in any of the prior art compounds or in the claims of the '293 Patent. Expert Report of Dr. William Hargrove, paragraphs 34-47."""
    },
    # Section 6: Statement of Facts (Part 3)
    {
        "title": "",
        "content": """E. The Regulatory and Market Context

Following FDA approval in September 2024, Pinnacle launched Cardiovan commercially in November 2024. Within four months, Cardiovan was prescribed to approximately 12,400 patients across 847 treatment centers in the United States. Clinical data from the Phase III CARDIAC-7 trial demonstrated that Cardiovan achieved superior rhythm control compared to amiodarone, the current standard of care, with a significantly lower incidence of pulmonary toxicity and thyroid dysfunction. Harrington Decl., Exhibit G.

The atrial fibrillation therapeutic market represents approximately $8.2 billion in annual United States revenue. Plaintiff's Rhythmex currently holds approximately 18% market share, generating annual revenues of approximately $1.47 billion. Since Cardiovan's launch, Plaintiff's market share has declined by approximately 2.3 percentage points, from 18% to approximately 15.7%. However, this decline is attributable to multiple competitive factors, including the entry of generic formulations of two other branded products and increased formulary restrictions imposed by pharmacy benefit managers. Expert Report of Dr. Rebecca Thornton, paragraphs 18-29.

Notably, Plaintiff did not take any action to enforce the '293 Patent until January 2025, more than fourteen months after learning of Pinnacle's FDA approval and three months after Cardiovan's commercial launch. During this period, Plaintiff continued to report record quarterly revenues and never communicated any infringement concerns to Defendant. Harrington Decl., paragraphs 12-15.

F. Procedural History

Plaintiff filed this action on January 28, 2025, asserting claims of patent infringement and seeking both monetary damages and injunctive relief. On February 14, 2025, Plaintiff filed the instant motion for preliminary injunction. Defendant filed counterclaims seeking declaratory judgments of invalidity and non-infringement on March 1, 2025."""
    },
    # Section 7: Argument Introduction
    {
        "title": "ARGUMENT",
        "content": """A party seeking a preliminary injunction must establish four elements: (1) a likelihood of success on the merits; (2) that it is likely to suffer irreparable harm in the absence of preliminary relief; (3) that the balance of equities tips in its favor; and (4) that an injunction is in the public interest. Winter v. Natural Resources Defense Council, Inc., 555 U.S. 7, 20 (2008). The movant bears the burden of making a clear showing on each of these elements. Id.

In the patent context, the Federal Circuit has emphasized that preliminary injunctive relief is an extraordinary remedy that should not be routinely granted. Amazon.com, Inc. v. Barnesandnoble.com, Inc., 239 F.3d 1343, 1350 (Fed. Cir. 2001). Following the Supreme Court's decision in eBay Inc. v. MercExchange, L.L.C., 547 U.S. 388 (2006), district courts must apply the traditional four-factor test and may not presume irreparable harm from patent infringement alone.

As demonstrated below, Plaintiff fails to satisfy any of the four required elements, and the motion should therefore be denied."""
    },
    # Section 8: Argument I.A - Patent Invalid
    {
        "title": "I. PLAINTIFF CANNOT DEMONSTRATE A LIKELIHOOD OF SUCCESS ON THE MERITS",
        "content": """A. The Patent Claims Are Invalid Under 35 U.S.C. Section 103

Under 35 U.S.C. Section 103, a patent claim is invalid if the differences between the claimed invention and the prior art are such that the subject matter as a whole would have been obvious to a person having ordinary skill in the art at the time of the invention. Graham v. John Deere Co., 383 U.S. 1, 17-18 (1966). The Supreme Court in KSR International Co. v. Teleflex Inc., 550 U.S. 398 (2007), rejected a rigid application of the teaching-suggestion-motivation test and held that the obviousness analysis must consider the broader context of the prior art.

1. The Nakamura Reference Discloses the Core Compound

The Nakamura publication, dated 2015, discloses 2,3-disubstituted benzofuran compounds with C-5 functional groups that are structurally identical to the compounds described in Formula I of the '293 Patent. Specifically, Nakamura's Compound 14b contains the same benzofuran scaffold, the same substitution pattern at the 2- and 3-positions, and the same C-5 methoxy group recited in the patent claims. The only structural difference between Nakamura's Compound 14b and the claimed compound is the substitution at the C-7 position.

Dr. Hargrove, Defendant's expert in pharmaceutical chemistry, has opined that a person of ordinary skill in the art would have understood that the C-5 methoxy substitution disclosed in Nakamura provides the critical pharmacological activity claimed in the '293 Patent, specifically the selective modulation of hERG potassium channel conductance. Hargrove Expert Report, paragraphs 52-58.

2. The Chen Reference Teaches the C-7 Modification

The remaining structural element claimed in the '293 Patent, the C-7 hydroxyl group, is explicitly taught by the Chen reference. Chen identified the C-7 position as a key determinant of selectivity between cardiac ion channel subtypes and disclosed several C-7 hydroxyl analogs with superior therapeutic indices compared to unsubstituted compounds. Chen specifically noted that C-7 hydroxylation of benzofuran derivatives "enhances selectivity for cardiac potassium channels over sodium channels by approximately five-fold" (Chen at 1894).

A person of ordinary skill in the art, motivated by the desire to improve the selectivity and therapeutic index of Nakamura's Compound 14b, would have been motivated to combine Nakamura's disclosure with Chen's teaching regarding C-7 hydroxylation. The combination would have yielded the precise compound claimed in the '293 Patent with a reasonable expectation of success."""
    },
    # Section 9: Argument I.A continued
    {
        "title": "",
        "content": """3. The Bergstrom Reference Teaches the Sustained-Release Formulation

The claim limitation requiring a pharmaceutical composition that "provides a sustained plasma concentration over a period of at least twelve hours" is directly taught by the Bergstrom European patent application. Bergstrom discloses the use of hydroxypropyl methylcellulose matrices specifically designed to achieve twelve-hour sustained-release pharmacokinetic profiles for benzofuran-based active pharmaceutical ingredients.

Plaintiff may argue that Bergstrom's formulation technology was not specifically applied to the compound of Formula I. However, it is well-established that the adaptation of known formulation techniques to a structurally related compound does not constitute a patentable advance when the combination would have been predictable to a skilled artisan. See Abbott Laboratories v. Sandoz, Inc., 566 F.3d 1282, 1297 (Fed. Cir. 2009) (holding that routine formulation optimization does not confer patentability).

4. Objective Indicia Do Not Overcome the Strong Prima Facie Case

Plaintiff may attempt to rely on objective indicia of nonobviousness, such as commercial success and unexpected results. However, any such evidence is insufficient to overcome the strong prima facie case of obviousness established by the combination of Nakamura, Chen, and Bergstrom.

First, the commercial success of Rhythmex does not establish nonobviousness because Plaintiff has not demonstrated a nexus between the claimed invention and the commercial success. Rhythmex's market performance is attributable to Plaintiff's extensive marketing expenditures (approximately $340 million annually), favorable formulary positioning, and first-mover advantage in the sustained-release atrial fibrillation segment. These marketplace factors, rather than the novelty of the underlying compound, account for Rhythmex's commercial success.

Second, Plaintiff's assertion of unexpected results is undermined by the prior art itself. The pharmacological properties attributed to the claimed compound, including selective hERG potassium channel modulation and sustained-release oral bioavailability, were precisely the properties predicted by the prior art references. The Nakamura reference reported hERG selectivity data, and the Chen reference quantified the selectivity improvement from C-7 hydroxylation. There is nothing "unexpected" about achieving results that were explicitly predicted in the literature."""
    },
    # Section 10: Argument I.B - Non-Infringement
    {
        "title": "B. Defendant's Product Does Not Infringe",
        "content": """Even assuming the validity of the '293 Patent, Plaintiff cannot demonstrate a likelihood of success on its infringement claim. Proper claim construction, guided by the intrinsic evidence, establishes that Defendant's Cardiovan product does not practice the claimed invention.

1. Claim Construction Principles

Claim terms must be given their ordinary and customary meaning as understood by a person of ordinary skill in the art at the time of the invention, in light of the intrinsic evidence, including the claims, specification, and prosecution history. Phillips v. AWH Corp., 415 F.3d 1303, 1312-13 (Fed. Cir. 2005) (en banc).

2. The "Therapeutically Effective Amount" Limitation

Claim 1 requires "a therapeutically effective amount of a compound having the structural formula described in Formula I." The specification defines this term as referring to "an amount sufficient to achieve measurable inhibition of hERG potassium channel conductance in cardiac tissue" (col. 4, lines 32-35). This definition limits the claim to compounds that operate through the specific mechanism of hERG channel inhibition.

Defendant's Cardiovan product operates through a fundamentally different mechanism. While the compound PPC-4892 does contain a benzofuran scaffold, its primary therapeutic effect is mediated through modulation of calcium-activated potassium channels rather than hERG channels. The expert testimony of Dr. Hargrove establishes that PPC-4892 has less than 5% activity at the hERG potassium channel at therapeutic concentrations, compared to greater than 85% activity at calcium-activated potassium channels. Hargrove Expert Report, paragraphs 67-74.

Under the proper construction of "therapeutically effective amount," which requires measurable hERG channel inhibition, Defendant's product does not satisfy this claim limitation because PPC-4892 does not achieve therapeutically meaningful hERG channel modulation at the doses prescribed for atrial fibrillation treatment."""
    },
    # Section 11: Argument I.B continued
    {
        "title": "",
        "content": """3. The "Structural Formula Described in Formula I" Limitation

Plaintiff's infringement theory also fails with respect to the structural formula limitation. The compound PPC-4892 differs from Formula I in a critical structural respect: PPC-4892 contains a C-4 amide linkage that replaces the C-4 hydrogen present in Formula I. This structural modification fundamentally alters the three-dimensional conformation of the molecule and its binding characteristics.

Dr. Hargrove's molecular modeling analysis demonstrates that the C-4 amide group in PPC-4892 creates an intramolecular hydrogen bond that stabilizes a folded molecular conformation. This conformation is geometrically incompatible with binding to the hERG channel pore domain but is optimally configured for interaction with the calcium-activated potassium channel selectivity filter. Hargrove Expert Report, paragraphs 75-83.

Plaintiff may argue that the C-4 amide modification is an insubstantial difference under the doctrine of equivalents. However, the doctrine of equivalents cannot be applied to capture structural features that were specifically distinguished during prosecution. As discussed in Section I.C below, the prosecution history estoppel arising from Plaintiff's amendments during patent examination precludes application of the doctrine of equivalents to the C-4 position.

4. Dependent Claims 7, 12, and 18

The dependent claims add further limitations that Defendant's product does not satisfy. Claim 7 requires a specific dissolution profile in 0.1N hydrochloric acid, which Defendant's product does not exhibit due to its enteric coating formulation. Claim 12 requires administration in conjunction with a beta-adrenergic receptor antagonist, which is not part of Defendant's approved labeling or prescribing information. Claim 18 requires a specific particle size distribution that is not present in PPC-4892's crystalline form. Declaration of Dr. James Whitfield, paragraphs 14-22."""
    },
    # Section 12: Argument I.C - Prosecution History Estoppel
    {
        "title": "C. Prosecution History Estoppel Bars Plaintiff's Infringement Claims",
        "content": """The prosecution history of the '293 Patent confirms that Plaintiff's broad infringement theory must be rejected. During prosecution, the examiner rejected the original claims as obvious over the combination of Nakamura and a reference by Taniguchi that disclosed benzofuran compounds with various C-4 substitutions, including amide groups.

In response to this rejection, Plaintiff's patent counsel narrowed the claims by adding limitations specifying that the compound of Formula I contains an unsubstituted C-4 position. The prosecution history file wrapper clearly documents the following exchange:

Amendment dated April 12, 2020: "Applicant respectfully traverses the rejection and amends independent Claim 1 to specify that the compound of Formula I has an unsubstituted C-4 carbon position. The Taniguchi reference relies entirely on C-4 substituted benzofuran derivatives. The claimed compounds are distinguished from Taniguchi because they specifically exclude C-4 substitutions, which, as explained in the specification at paragraphs 47-52, would interfere with the critical hERG channel binding interaction."

This amendment and the accompanying arguments constitute a clear and unmistakable surrender of claim scope encompassing C-4 substituted compounds. Because Defendant's PPC-4892 contains a C-4 amide substitution, prosecution history estoppel bars Plaintiff from asserting infringement under either literal infringement or the doctrine of equivalents.

The estoppel applies even if Plaintiff could demonstrate that the C-4 amide performs substantially the same function in substantially the same way to achieve substantially the same result. The Supreme Court has held that when a claim amendment is made for patentability reasons, there is a presumption that the amendment surrendered the territory between the original claim and the amended claim, and this presumption can only be rebutted in narrow circumstances not present here."""
    },
    # Section 13: Argument II - Irreparable Harm
    {
        "title": "II. PLAINTIFF CANNOT SHOW IRREPARABLE HARM",
        "content": """Even if Plaintiff could establish a likelihood of success on the merits, the motion should be denied because Plaintiff has failed to demonstrate that it will suffer irreparable harm absent injunctive relief.

A. Plaintiff's Delay Undermines Its Claim of Irreparable Harm

Plaintiff's fourteen-month delay between learning of Defendant's product and seeking injunctive relief severely undermines any claim of urgency or irreparable injury. Plaintiff became aware of Defendant's FDA approval in September 2024 through publicly available FDA announcements and industry publications. Despite this knowledge, Plaintiff took no enforcement action until January 2025 and did not file the instant motion until February 2025.

Courts in this Circuit and throughout the country have consistently held that unexplained delays in seeking preliminary injunctive relief weigh against a finding of irreparable harm. A delay of even a few months has been found sufficient to defeat a claim of irreparable injury in patent cases. Here, the fourteen-month delay from knowledge of FDA approval to the filing of the preliminary injunction motion is substantial and unexplained.

Plaintiff's argument that it was conducting an investigation during this period is unpersuasive. Plaintiff is a sophisticated pharmaceutical company with an extensive in-house legal department and access to outside counsel with expertise in patent litigation. The allegedly infringing product was publicly available for analysis from the date of FDA approval. There is no credible explanation for why a preliminary investigation would require fourteen months.

B. Plaintiff's Harm Is Compensable Through Monetary Damages

The harm that Plaintiff alleges, loss of market share and decreased revenues, is precisely the type of injury that is fully compensable through an award of monetary damages. Plaintiff's own expert, Dr. Thornton, has quantified the alleged revenue impact at approximately $38.4 million over the relevant period. This calculation demonstrates that the harm is capable of precise monetary quantification and therefore does not constitute the type of irreparable injury that warrants the extraordinary remedy of preliminary injunctive relief.

Moreover, Defendant is a solvent, profitable company with substantial assets and insurance coverage sufficient to satisfy any damages judgment. There is no risk that Plaintiff will be unable to collect damages if it ultimately prevails on the merits."""
    },
    # Section 14: Argument II continued
    {
        "title": "",
        "content": """C. Plaintiff Has Not Demonstrated Loss of Market Position or Goodwill

Plaintiff's assertion that it will suffer irreparable harm through loss of market position and customer goodwill is speculative and unsupported by the record. The pharmaceutical market for atrial fibrillation therapeutics is not a two-competitor market. There are currently seven FDA-approved treatments for atrial fibrillation, including generic formulations. Plaintiff's market share fluctuations are influenced by multiple competitive dynamics, including insurance coverage decisions, physician prescribing preferences, clinical trial data from competing products, and generic competition.

Dr. Thornton's analysis concedes that approximately 60% of Plaintiff's recent market share decline is attributable to factors unrelated to Defendant's product, including the entry of generic formulations and changes in pharmacy benefit manager formularies. The remaining 40% of the decline, representing approximately 0.9 percentage points of market share, is insufficient to establish the type of irreparable market disruption that would justify the extraordinary remedy of a preliminary injunction.

Furthermore, Plaintiff has not presented any evidence that the loss of customer relationships or physician prescribing habits would be permanent or irreversible. Physicians regularly adjust prescribing patterns based on clinical evidence, insurance coverage, and patient response. If Plaintiff ultimately prevails in this litigation and obtains a permanent injunction, there is no reason to believe that physicians would not resume prescribing Rhythmex to appropriate patients.

D. Plaintiff's Licensing Activities Undermine Its Irreparable Harm Claim

The record shows that Plaintiff has actively licensed the '293 Patent to two other pharmaceutical companies, Vertex Therapeutics and Catalent Pharma Solutions, for royalty payments. These licensing arrangements demonstrate that Plaintiff views the '293 Patent primarily as a revenue-generating asset rather than an exclusionary right essential to maintaining its competitive position. A patentee that willingly licenses its patent to competitors cannot credibly claim that additional competition from Defendant causes irreparable harm."""
    },
    # Section 15: Argument III - Balance of Equities
    {
        "title": "III. THE BALANCE OF EQUITIES FAVORS DEFENDANT",
        "content": """The balance of equities weighs decisively against the issuance of a preliminary injunction. The harm that Defendant and third parties would suffer from an injunction substantially outweighs any potential benefit to Plaintiff.

A. Harm to Defendant

A preliminary injunction would effectively destroy Defendant's cardiovascular therapeutics business. Pinnacle invested more than $420 million in the development of Cardiovan over a period of eight years, including approximately $180 million in clinical trial costs alone. An injunction requiring Defendant to withdraw Cardiovan from the market would render this investment worthless and would likely result in substantial workforce reductions affecting more than 600 employees at Defendant's Baltimore research facility and manufacturing plant.

Moreover, Defendant has entered into supply agreements with major pharmaceutical distributors and hospital systems with contractual obligations totaling approximately $890 million over the next three years. An injunction would put Defendant in immediate breach of these agreements, exposing it to significant third-party liability and reputational harm that could impair its ability to develop and market future products.

B. Harm to Healthcare Providers and Patients

An injunction would disrupt ongoing treatment for approximately 12,400 patients currently prescribed Cardiovan. Abrupt discontinuation of anti-arrhythmic medication poses serious health risks, including breakthrough arrhythmias, hemodynamic instability, and in severe cases, stroke or cardiac arrest. The American Heart Association guidelines specifically caution against sudden withdrawal of anti-arrhythmic therapy without adequate transition planning.

Treating physicians would face the difficult task of transitioning thousands of patients to alternative medications, many of which have demonstrated inferior efficacy or higher adverse effect profiles in clinical trials. The CARDIAC-7 trial showed that Cardiovan achieved a 23% relative improvement in sustained sinus rhythm maintenance compared to the next most effective available alternative, with a 47% reduction in the incidence of serious adverse events including pulmonary fibrosis and thyroid dysfunction."""
    },
    # Section 16: Argument III continued
    {
        "title": "",
        "content": """C. Harm to the Competitive Marketplace

The pharmaceutical market for atrial fibrillation treatment benefits from competition that drives innovation, improves patient access, and constrains pricing. Removing Cardiovan from the market would reduce the number of available therapeutic options and eliminate competitive pressure that has contributed to recent price moderation in this market segment.

Since Cardiovan's entry, the average wholesale acquisition cost for atrial fibrillation medications in the sustained-release category has decreased by approximately 8.4%, representing significant savings for patients, insurers, and the healthcare system. An injunction that removes this competitive pressure would likely result in price increases that disproportionately affect underserved patient populations.

D. The Equities Do Not Support Maintaining the Status Quo

Plaintiff argues that a preliminary injunction would simply maintain the "status quo" that existed before Cardiovan's market entry. This characterization is misleading. The relevant status quo is the current state of affairs, not some hypothetical pre-competition scenario. The current status quo includes 12,400 patients receiving Cardiovan, hundreds of healthcare providers who have integrated Cardiovan into their treatment protocols, and a functioning supply chain that serves the needs of patients and institutions across the country.

Disrupting this established status quo through a preliminary injunction would cause immediate and concrete harm to real patients and healthcare providers. By contrast, maintaining the current status quo while this litigation proceeds to resolution on the merits would preserve access to medication while allowing the parties to fully develop the factual record regarding validity and infringement.

Plaintiff has adequate alternative remedies available during the pendency of this litigation. It can pursue expedited discovery, seek an early claim construction ruling, and move for summary judgment on clearly defined issues. If Plaintiff ultimately prevails, it will be entitled to damages and can seek a permanent injunction following a full adjudication on the merits."""
    },
    # Section 17: Argument IV - Public Interest
    {
        "title": "IV. THE PUBLIC INTEREST WEIGHS AGAINST INJUNCTION",
        "content": """The final factor in the preliminary injunction analysis, the public interest, weighs strongly against the requested relief. While the public has an interest in enforcing valid patent rights, that interest must be balanced against other significant public interests, particularly when pharmaceutical products and patient health are at stake.

A. Access to Critical Medications

The public interest in continued access to safe, effective medications is paramount. Cardiovan has been demonstrated through rigorous clinical trials to offer significant therapeutic advantages over existing treatments for atrial fibrillation. The CARDIAC-7 trial, a randomized, double-blind, multi-center study involving 4,832 patients, showed that Cardiovan achieved a 67.3% rate of sustained sinus rhythm maintenance at twelve months, compared to 54.7% for amiodarone and 49.2% for dronedarone.

More importantly, Cardiovan demonstrated a markedly superior safety profile. The incidence of pulmonary toxicity, the most serious adverse effect associated with amiodarone (the current standard of care), was 0.3% in the Cardiovan group compared to 7.2% in the amiodarone group. Similarly, the incidence of thyroid dysfunction was 1.1% for Cardiovan versus 14.6% for amiodarone. These safety advantages translate into real clinical benefits for patients who require long-term anti-arrhythmic therapy.

Removing such a medication from the market based on a preliminary assessment of patent rights, particularly when the validity of those rights is seriously in doubt, would disserve the public interest in the strongest terms.

B. The Public Interest in Innovation and Competition

The patent system is designed to promote innovation by granting limited monopoly rights in exchange for public disclosure. However, the system also recognizes that overbroad enforcement of patent rights can stifle innovation by preventing competitors from developing improved products. The issuance of a preliminary injunction based on patent claims whose validity is questionable would send a chilling signal to pharmaceutical companies investing in the development of next-generation cardiovascular therapeutics."""
    },
    # Section 18: Argument IV continued
    {
        "title": "",
        "content": """C. Regulatory Considerations

The FDA's approval of Cardiovan reflects a comprehensive regulatory determination that the product is safe and effective for its intended use. While FDA approval does not immunize a product from patent infringement claims, it does represent a significant governmental judgment about the public health value of the medication. A preliminary injunction that effectively countermands this regulatory determination should be issued only upon a clear and convincing showing that the patent rights at issue are valid and infringed. No such showing has been made here.

Furthermore, the FDA has designated Cardiovan as the only available alternative for patients who are intolerant to amiodarone and who are not candidates for catheter ablation. Approximately 2,100 patients currently prescribed Cardiovan fall into this clinical category. For these patients, removal of Cardiovan from the market would leave them with no adequate therapeutic alternative, a result that cannot be reconciled with the public interest.

D. Healthcare System Costs

The economic impact of an injunction on the broader healthcare system must also be considered. The transition of 12,400 patients from Cardiovan to alternative therapies would require extensive medical monitoring, including baseline and follow-up electrocardiograms, thyroid function tests, pulmonary function assessments, and hepatic function panels. The estimated aggregate cost of these transition-related medical services exceeds $18.7 million, which would be borne by patients, insurers, and government healthcare programs.

Additionally, the inferior tolerability of alternative agents would likely result in increased hospitalization rates. Historical data indicates that patients transitioning between anti-arrhythmic medications experience a 12.3% rate of arrhythmia-related hospitalization during the transition period, compared to 3.1% for patients maintained on stable therapy. The projected excess hospitalizations would cost an estimated $31.2 million and represent a significant burden on already-strained healthcare resources."""
    },
    # Section 19: Conclusion
    {
        "title": "CONCLUSION",
        "content": """For the foregoing reasons, Defendant Pinnacle Pharmaceuticals Corp. respectfully requests that this Court deny Plaintiff's motion for a preliminary injunction in its entirety.

Plaintiff has failed to establish any of the four requirements for preliminary injunctive relief. The asserted patent claims are likely invalid as obvious over the combination of the Nakamura, Chen, and Bergstrom prior art references. Defendant's product does not infringe the properly construed claims. Plaintiff cannot demonstrate irreparable harm given its fourteen-month delay in seeking relief and the compensability of its alleged injuries. The balance of equities and the public interest overwhelmingly favor continued public access to Cardiovan while this matter proceeds to resolution on the merits.

In the alternative, should the Court determine that some form of preliminary relief is warranted, Defendant respectfully requests that the Court require Plaintiff to post a substantial bond pursuant to Federal Rule of Civil Procedure 65(c) in an amount sufficient to cover Defendant's losses in the event the injunction is later found to have been wrongfully issued. Given the magnitude of the potential harm to Defendant, its employees, patients, and the healthcare system, Defendant submits that a bond in the amount of $500 million would be appropriate.

WHEREFORE, Defendant Pinnacle Pharmaceuticals Corp. respectfully requests that this Court:

1. Deny Plaintiff's motion for a preliminary injunction;

2. In the alternative, require Plaintiff to post a bond of not less than $500 million;

3. Award Defendant its costs and attorneys' fees incurred in opposing this motion; and

4. Grant such other and further relief as this Court deems just and proper.

Respectfully submitted,

BLACKSTONE & WHITFIELD LLP


By: _________________________________
    Katherine M. Harrington, Esq. (Bar No. KH-4892)
    Daniel R. Ostrowski, Esq. (Bar No. DO-7231)
    1200 Avenue of the Americas, 38th Floor
    New York, NY 10036
    Telephone: (212) 555-4800
    Facsimile: (212) 555-4801
    Email: k.harrington@blackstonewhitfield.com
           d.ostrowski@blackstonewhitfield.com

    Counsel for Defendant Pinnacle
    Pharmaceuticals Corp.

Dated: March 15, 2025"""
    },
    # Section 20: Certificate of Service
    {
        "title": "CERTIFICATE OF SERVICE",
        "content": """I hereby certify that on March 15, 2025, a true and correct copy of the foregoing DEFENDANT'S MEMORANDUM OF LAW IN OPPOSITION TO PLAINTIFF'S MOTION FOR PRELIMINARY INJUNCTION was served upon the following counsel of record via the Court's CM/ECF electronic filing system:

Robert A. Castellano, Esq.
Michelle T. Bradford, Esq.
MORRISON & STERLING LLP
800 Third Avenue, Suite 2600
New York, NY 10022
r.castellano@morrisonsterling.com
m.bradford@morrisonsterling.com
Counsel for Plaintiff Meridian Healthcare Systems, Inc.


_________________________________
Katherine M. Harrington, Esq.
BLACKSTONE & WHITFIELD LLP"""
    },
]

def create_initial():
    os.makedirs(BRIEF_DIR, exist_ok=True)

    doc = pymupdf.open()

    # Page layout constants
    PAGE_W, PAGE_H = 612, 792  # Letter size
    MARGIN_LEFT = 72
    MARGIN_RIGHT = 540
    MARGIN_TOP = 72
    MARGIN_BOTTOM = 720
    TEXT_WIDTH = MARGIN_RIGHT - MARGIN_LEFT
    LINE_HEIGHT = 14
    HEADING_SIZE = 14
    BODY_SIZE = 11
    FOOTER_SIZE = 9

    page_number = 0

    for section in BRIEF_SECTIONS:
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_number += 1
        y = MARGIN_TOP

        # Section title
        if section["title"]:
            page.insert_text(
                pymupdf.Point(MARGIN_LEFT, y + HEADING_SIZE),
                section["title"],
                fontsize=HEADING_SIZE,
                fontname="hebo",
                color=(0, 0, 0),
            )
            y += HEADING_SIZE + 20

        # Body text in textbox
        content = section["content"].strip()
        text_rect = pymupdf.Rect(MARGIN_LEFT, y, MARGIN_RIGHT, MARGIN_BOTTOM)
        excess = page.insert_textbox(
            text_rect,
            content,
            fontsize=BODY_SIZE,
            fontname="tiro",
            color=(0, 0, 0),
            align=pymupdf.TEXT_ALIGN_JUSTIFY,
        )

        # Add page number footer
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - 36),
            str(page_number),
            fontsize=FOOTER_SIZE,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

        # Note: insert_textbox returns a float (negative=all fit, positive=overflow length).
        # We cannot recover excess text, so each section simply fits what it can on one page.

    # Pad to ensure ~30 pages with additional content if needed
    while doc.page_count < 30:
        page = doc.new_page(width=PAGE_W, height=PAGE_H)
        page_number += 1

        # Add exhibit placeholder pages
        exhibit_num = doc.page_count - 20
        page.insert_text(
            pymupdf.Point(MARGIN_LEFT, MARGIN_TOP + HEADING_SIZE),
            f"EXHIBIT {chr(64 + min(exhibit_num, 26))}",
            fontsize=HEADING_SIZE,
            fontname="hebo",
            color=(0, 0, 0),
        )

        exhibit_texts = [
            "Declaration of Katherine M. Harrington, Esq., including attached correspondence between counsel for the parties dated October through December 2024, FDA approval letter for Cardiovan dated September 12, 2024, and market share analysis prepared by Thomson Healthcare Analytics.",
            "Expert Report of Dr. William Hargrove, Ph.D., Professor of Pharmaceutical Chemistry, Johns Hopkins University School of Medicine, including structural analysis of PPC-4892, molecular modeling comparisons with Formula I compounds, and ion channel binding assay results.",
            "Expert Report of Dr. Rebecca Thornton, Ph.D., Professor of Health Economics, Columbia University Mailman School of Public Health, including market impact analysis, revenue projections, and competitive landscape assessment for the atrial fibrillation therapeutics market.",
            "Declaration of Dr. James Whitfield, Director of Pharmaceutical Sciences, Pinnacle Pharmaceuticals Corp., regarding the dissolution profile, particle size distribution, and formulation characteristics of Cardiovan tablets.",
            "Certified copies of the prosecution history file wrapper for U.S. Patent No. 10,847,293, including all office actions, applicant responses, amendments, and examiner interviews.",
            "Clinical trial results from the CARDIAC-7 Phase III randomized controlled trial, including primary and secondary endpoint analyses, subgroup analyses, safety data tables, and Kaplan-Meier survival curves for sustained sinus rhythm maintenance.",
            "Affidavit of Dr. Samantha Reeves, Vice President of Research and Development, Pinnacle Pharmaceuticals Corp., regarding the independent development timeline of PPC-4892 and Cardiovan, including laboratory notebooks, research proposals, and milestone documentation.",
            "Copies of license agreements between Meridian Healthcare Systems, Inc. and Vertex Therapeutics, Inc. and between Meridian Healthcare Systems, Inc. and Catalent Pharma Solutions, Inc., for the licensed use of technology covered by U.S. Patent No. 10,847,293.",
            "American Heart Association Guidelines for the Management of Patients with Atrial Fibrillation, including recommendations regarding anti-arrhythmic drug therapy transitions and monitoring protocols during medication changes.",
            "Financial analysis prepared by Deloitte Consulting LLP regarding the economic impact of Cardiovan market withdrawal, including projected costs for patient transition, healthcare utilization, and workforce effects at Pinnacle Pharmaceuticals Corp.",
        ]

        exhibit_idx = exhibit_num - 1
        if 0 <= exhibit_idx < len(exhibit_texts):
            text_rect = pymupdf.Rect(MARGIN_LEFT, MARGIN_TOP + 50, MARGIN_RIGHT, MARGIN_BOTTOM)
            page.insert_textbox(
                text_rect,
                exhibit_texts[exhibit_idx],
                fontsize=BODY_SIZE,
                fontname="tiro",
                color=(0, 0, 0),
                align=pymupdf.TEXT_ALIGN_LEFT,
            )

        # Page number
        page.insert_text(
            pymupdf.Point(PAGE_W / 2 - 10, PAGE_H - 36),
            str(page_number),
            fontsize=FOOTER_SIZE,
            fontname="tiro",
            color=(0.4, 0.4, 0.4),
        )

    # Set metadata
    doc.set_metadata({
        "title": "Defendant's Memorandum in Opposition to Motion for Preliminary Injunction",
        "author": "Blackstone & Whitfield LLP",
        "subject": "Meridian Healthcare Systems v. Pinnacle Pharmaceuticals - Case No. 2025-CV-04382",
        "keywords": "patent, pharmaceutical, preliminary injunction, opposition brief",
        "creator": "Legal Document System",
    })

    # Add Table of Contents bookmarks
    toc = [
        [1, "Cover Page", 1],
        [1, "Table of Contents", 2],
        [1, "Table of Authorities", 3],
        [1, "Preliminary Statement", 4],
        [1, "Statement of Facts", 5],
        [1, "Argument", 8],
        [2, "I. Likelihood of Success on Merits", 9],
        [2, "II. Irreparable Harm", 14],
        [2, "III. Balance of Equities", 16],
        [2, "IV. Public Interest", 18],
        [1, "Conclusion", 20],
    ]
    doc.set_toc(toc)

    doc.save(OUTPUT)
    doc.close()
    print(f'Initial file created: {OUTPUT}')
    print(f'Total pages: {page_number}')

    # Ensure word_analysis.txt does NOT exist
    analysis_file = f'{BRIEF_DIR}/word_analysis.txt'
    if os.path.exists(analysis_file):
        os.remove(analysis_file)

    # GUI-ready startup
    launch_gui(f'evince "{OUTPUT}"', delay_sec=2.0)
    print('GUI_READY: launched evince with DISPLAY=:0')

create_initial()
