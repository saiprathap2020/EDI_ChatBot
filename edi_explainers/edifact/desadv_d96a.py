segment_explanations_d96a = {
    "UNB": {
        "explanation": "The Interchange Header segment defines the interchange’s metadata, identifying the sender and recipient (e.g., using GLN or DUNS), preparation date/time, and a unique interchange control reference. It specifies syntax rules (e.g., UNOC character set) and the application reference (e.g., DESADV).",
        "usage": "Mandatory (M, an..4 for syntax identifier; M, an..35 for sender/recipient IDs; M, an..14 for control reference), Interchange Level, MaxOcc: 1. Example: UNB+UNOC:3+1234567890123:14+9876543210987:14+241106:1200+000000001++DESADV."
    },
    "UNH": {
        "explanation": "Marks the start of the DESADV D96A message with a unique reference number, message type (DESADV), version (D), release (96A), controlling agency (UN), and association code (A01051).",
        "usage": "Mandatory (M, an..14 for reference number; M, an..6 for message type), Level 0, MaxOcc: 1. Example: UNH+00001+DESADV:D:96A:UN:A01051."
    },
    "BGM": {
        "explanation": "Defines the document as a despatch advice (code 351), assigns a unique despatch advice number, and specifies the message function (e.g., 9 for original).",
        "usage": "Mandatory (M, an..3 for document code; R, an..35 for despatch advice number), Level 0, MaxOcc: 1. Example: BGM+351+123456789+9."
    },
    "DTM": {
        "explanation": "Specifies the despatch advice issuance date/time (qualifier 137) in CCYYMMDD (102) format, indicating when the DESADV was created.",
        "usage": "Required (R, an..3 for qualifier; R, an..12 for date), Level 1, MaxOcc: 1. Example: DTM+137:20241106:102. Note: Inferred from message structure and EDIFACT standard, as not detailed in provided document."
    },
    "MEA+WT": {
        "explanation": "Specifies the total consignment goods gross weight (qualifier WT), including all packages and contents, in a specified unit (e.g., kilograms).",
        "usage": "Optional (O, an..3 for measurement qualifier; R, n..18 for value), Level 1, MaxOcc: 5. Example: MEA+WT+G+KGM:1500. Note: Inferred from message structure (MEA MaxOcc: 5) and EDIFACT standard."
    },
    "MEA+VOL": {
        "explanation": "Specifies the total consignment goods volume (qualifier VOL), including all packages, in a specified unit (e.g., cubic meters).",
        "usage": "Optional (O, an..3 for measurement qualifier; R, n..18 for value), Level 1, MaxOcc: 5. Example: MEA+VOL+V+MTQ:5.5. Note: Inferred from EDIFACT standard, as MEA allows multiple qualifiers."
    },
    "RFF+AAK": {
        "explanation": "References the despatch advice number (qualifier AAK), linking the DESADV to the shipment notification.",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+AAK:123456789. Note: Inferred from message structure and EDIFACT standard for transport reference."
    },
    "RFF+ON": {
        "explanation": "References the purchase order number (qualifier ON) from the DELFOR message, linking the despatch to a specific order at the header level.",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+ON:PO123456. Note: Inferred from EDIFACT standard, as RFF may include order references."
    },
    "NAD+CS": {
        "explanation": "Identifies the consignor (qualifier CS), the party dispatching the goods, using a coded party identifier (e.g., GLN or Volvo-assigned ID).",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+CS+SUPPLIER001::92. Note: From message structure (Consignor)."
    },
    "NAD+SE": {
        "explanation": "Identifies the seller (qualifier SE), the supplier responsible for the goods, using a coded party identifier.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+SE+2003::92. Note: From message structure (Seller)."
    },
    "NAD+CN": {
        "explanation": "Identifies the consignee (qualifier CN), the destination (e.g., Volvo Cars plant or warehouse), using a coded party identifier.",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+CN+BP2TD::92. Note: From message structure (Consignee)."
    },
    "NAD+CA": {
        "explanation": "Identifies the carrier (qualifier CA), the transport company responsible for delivering the goods.",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+CA+CARRIER001::92. Note: From message structure (Carrier)."
    },
    "LOC+11": {
        "explanation": "Specifies the place/port of discharge (qualifier 11), the primary delivery location (e.g., a Volvo Cars plant), using a coded location ID.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..25 for location ID), Level 2, MaxOcc: 1. Example: LOC+11+TAV::92. Note: From message structure."
    },
    "EQD": {
        "explanation": "Specifies equipment details (e.g., trailer or container type) used in the transport, including equipment identification.",
        "usage": "Dependent (D, an..17 for equipment ID), Level 1, MaxOcc: 10. Example: EQD+TR+TRAILER001. Note: From message structure."
    },
    "CPS": {
        "explanation": "Specifies the consignment packing sequence, identifying the hierarchical level of packaging (e.g., pallet, box) within the despatch.",
        "usage": "Required (R, an..17 for hierarchical ID), Level 1, MaxOcc: 999. Example: CPS+1. Note: From message structure."
    },
    "PAC": {
        "explanation": "Describes the number and type of packages (e.g., pallets, boxes) in the consignment, including package type codes.",
        "usage": "Required (R, n..8 for number of packages; R, an..17 for package type), Level 2, MaxOcc: 999. Example: PAC+10++PAL. Note: From message structure."
    },
    "QTY+52": {
        "explanation": "Specifies the number of packages (qualifier 52) in the consignment, as described in the PAC segment.",
        "usage": "Required (R, an..3 for qualifier; R, n..15 for quantity), Level 3, MaxOcc: 1. Example: QTY+52:10. Note: From message structure."
    },
    "PCI": {
        "explanation": "Identifies package markings (e.g., labels, barcodes) for tracking or handling instructions.",
        "usage": "Required (R, an..35 for marking instruction), Level 3, MaxOcc: 1000. Example: PCI+33E. Note: From message structure."
    },
    "RFF+PK": {
        "explanation": "References the package identification number (qualifier PK), linking the package to a specific identifier.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..35 for reference number), Level 4, MaxOcc: 1. Example: RFF+PK:PKG12345. Note: From message structure."
    },
    "GIR": {
        "explanation": "Provides related identification numbers (e.g., serial numbers, batch numbers) for items within a package.",
        "usage": "Required (R, an..35 for identification number), Level 4, MaxOcc: 99. Example: GIR+1+SER123:BJ. Note: From message structure."
    },
    "GIN+BJ": {
        "explanation": "Specifies the goods identity number (qualifier BJ, batch number) for items in the package.",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for identity number), Level 4, MaxOcc: 99. Example: GIN+BJ+BATCH001. Note: From message structure."
    },
    "LIN": {
        "explanation": "Identifies a specific item in the despatch using the buyer’s article number (Volvo Cars’ part number) from the DELFOR message.",
        "usage": "Required (R, an..35 for article number), Level 2, MaxOcc: 999. Example: LIN+++12345678:IN. Note: From message structure."
    },
    "PIA": {
        "explanation": "Provides additional item identifiers (e.g., supplier’s part number, drawing revision) to clarify specifications beyond the LIN segment.",
        "usage": "Dependent (D, an..35 for additional ID), Level 3, MaxOcc: 1. Example: PIA+1+SUP123:SA. Note: From message structure."
    },
    "QTY+12": {
        "explanation": "Specifies the despatched quantity (qualifier 12) of the item identified in the LIN segment, indicating the number of units shipped.",
        "usage": "Required (R, an..3 for qualifier; R, n..15 for quantity), Level 3, MaxOcc: 1. Example: QTY+12:100. Note: From message structure."
    },
    "ALI": {
        "explanation": "Provides additional information about the item (e.g., country of origin, customs status) for regulatory or logistical purposes.",
        "usage": "Required (R, an..3 for information code), Level 3, MaxOcc: 1. Example: ALI+US. Note: From message structure."
    },
    "GIN+ML": {
        "explanation": "Specifies the goods identity number (qualifier ML, serial number) for individual items in the despatch.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..35 for identity number), Level 3, MaxOcc: 100. Example: GIN+ML+SERIAL123. Note: From message structure."
    },
    "MOA": {
        "explanation": "Specifies monetary amounts (e.g., item value) associated with the despatch for financial or customs purposes.",
        "usage": "Dependent (D, n..18 for amount), Level 3, MaxOcc: 1. Example: MOA+203:1000. Note: From message structure."
    },
    "RFF+AEE": {
        "explanation": "References the despatch note number (qualifier AEE) associated with the line item, used for tracking shipments.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..35 for reference number), Level 3, MaxOcc: 1. Example: RFF+AEE:DESP123."
    },
    "RFF+IV": {
        "explanation": "References the invoice number (qualifier IV) associated with the line item, used for financial reconciliation.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..35 for reference number), Level 3, MaxOcc: 1. Example: RFF+IV:INV202411001."
    },
    "DTM+171": {
        "explanation": "Specifies the reference date/time (qualifier 171) for the despatch note or invoice (when RFF qualifier is AEE or IV), in CCYYMMDD format.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..8 for date), Level 4, MaxOcc: 1. Example: DTM+171:20241106:102."
    },
    "LOC+159": {
        "explanation": "Specifies an additional internal destination (qualifier 159), an internal delivery point within the consignee’s facility (e.g., dock or gate), printed on the transport label in the ‘Dock/Gate’ field, corresponding to DELFOR’s LOC+159.",
        "usage": "Required (R, an..3 for qualifier; R, an..12 for location ID), Level 3, MaxOcc: 1. Example: LOC+159+TVV::92."
    },
    "UNT": {
        "explanation": "Closes the message with a segment count and repeats the UNH reference number for integrity.",
        "usage": "Mandatory (M, n..6 for segment count; M, an..14 for reference), Level 0, MaxOcc: 1. Example: UNT+21+00001."
    },
    "UNZ": {
        "explanation": "The Interchange Trailer segment closes the interchange, specifying the number of messages and repeating the UNB control reference.",
        "usage": "Mandatory (M, n..6 for message count; M, an..14 for control reference), Interchange Level, MaxOcc: 1. Example: UNZ+1+000000001. Note: Inferred from EDIFACT standard, as not detailed in provided document."
    }
}

def explain_segment(segment):
    segment_info = segment_explanations_d96a.get(segment.upper(), None)
    if segment_info:
        return f"**Explanation**\n{segment_info['explanation']}\n\n**Usage**\n{segment_info['usage']}"
    return f"No explanation available for DESADV D96A segment {segment}."

def process(user_message):
    """
    Process a user message using DESADV_D96A specification.
    
    Args:
        user_message (str): The user's input message (e.g., 'UNH' or 'What is the UNH segment?').
    
    Returns:
        str: The formatted explanation of the segment.
    """
    # Parse the message to extract a segment code
    words = user_message.upper().split()
    segment = next((word for word in words if word in segment_explanations_d96a), None)
    if segment:
        return explain_segment(segment)
    return f"Could not find a valid segment code in your message: {user_message}"