segment_explanations_d07a = {
    "UNB": {
        "explanation": "The Interchange Header segment defines the interchange's metadata, identifying the sender and recipient (e.g., using GLN or DUNS), preparation date/time, and a unique interchange control reference. It specifies syntax rules (e.g., UNOC character set) and the application reference (e.g., DESADV) for processing the interchange.",
        "usage": "Mandatory (M, an..4 for syntax identifier; M, an..35 for sender/recipient IDs; M, an..14 for control reference), Interchange Level, MaxOcc: 1. Example: UNB+UNOC:3+1234567890123:14+9876543210987:14+250120:1000+000000001++DESADV."
    },
    "UNH": {
        "explanation": "Marks the start of the DESADV D07A message with a unique reference number, message type (DESADV), version (D), release (07A), controlling agency (UN), and association code (JAIF).",
        "usage": "Mandatory (M, an..14 for reference number; M, an..6 for message type), Level 0, MaxOcc: 1. Example: UNH+XFR151560+DESADV:D:07A:UN:JAIF."
    },
    "BGM": {
        "explanation": "Defines the document as a despatch advice (code 351), assigns a unique despatch advice number, and specifies the message function (e.g., 9 for original).",
        "usage": "Mandatory (M, an..3 for document code; R, an..35 for despatch advice number), Level 0, MaxOcc: 1. Example: BGM+351+123456789+9."
    },
    "DTM": {
        "explanation": "Specifies the despatch advice issuance date/time (qualifier 137) in CCYYMMDD (102) or CCYYMMDDHHMM (203) format, indicating when the DESADV was created.",
        "usage": "Required (R, an..3 for qualifier; R, an..12 for date), Level 1, MaxOcc: 1. Example: DTM+137:20250120:102."
    },
    "MEA+WT": {
        "explanation": "Specifies the total consignment goods gross weight (qualifier WT), including all packages and contents, in a specified unit (e.g., kilograms).",
        "usage": "Required (R, an..3 for measurement qualifier; R, n..18 for value), Level 1, MaxOcc: 1. Example: MEA+WT+G+KGM:1500."
    },
    "MEA+VOL": {
        "explanation": "Specifies the total consignment goods volume (qualifier VOL), including all packages, in a specified unit (e.g., cubic meters).",
        "usage": "Required (R, an..3 for measurement qualifier; R, n..18 for value), Level 1, MaxOcc: 1. Example: MEA+VOL+V+MTQ:5.5."
    },
    "MEA+FWT": {
        "explanation": "Specifies the container fare weight (qualifier FWT), the weight of the empty container, used when containers are involved in transport.",
        "usage": "Dependent (D, an..3 for measurement qualifier; R, n..18 for value), Level 1, MaxOcc: 1. Example: MEA+FWT++KGM:200."
    },
    "MEA+GWT": {
        "explanation": "Specifies the container gross weight (qualifier GWT), the total weight of the container including contents, used when containers are involved.",
        "usage": "Dependent (D, an..3 for measurement qualifier; R, n..18 for value), Level 1, MaxOcc: 1. Example: MEA+GWT++KGM:1700."
    },
    "RFF+AAK": {
        "explanation": "References the despatch advice number (qualifier AAK), linking the DESADV to the shipment notification.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+AAK:123456789."
    },
    "RFF+ON": {
        "explanation": "References the purchase order number (qualifier ON) from the DELFOR/DELJIT message, linking the despatch to a specific order at the header level.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..17 for reference number), Level 1, MaxOcc: 1. Example: RFF+ON:435912345020."
    },
    "RFF+IV": {
        "explanation": "References the invoice number (qualifier IV) associated with the despatch, used for financial reconciliation.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+IV:INV202501001."
    },
    "RFF+AAO": {
        "explanation": "References the transport order number (qualifier AAO), linking the despatch to logistics coordination.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+AAO:TRN202501001."
    },
    "RFF+ALF": {
        "explanation": "References the delivery schedule number (qualifier ALF) from the DELFOR message, connecting the despatch to the planned schedule.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+ALF:1000006440."
    },
    "RFF+AIT": {
        "explanation": "References the transport instruction number (qualifier AIT), specifying transport arrangements for the despatch.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for reference number), Level 1, MaxOcc: 1. Example: RFF+AIT:TI202501001."
    },
    "NAD+SE": {
        "explanation": "Identifies the seller (qualifier SE), the supplier dispatching the goods, using a coded party identifier (e.g., GLN or Volvo-assigned ID).",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+SE+2003::92."
    },
    "NAD+BY": {
        "explanation": "Identifies the buyer (qualifier BY), typically a Volvo Cars entity (e.g., purchasing unit or plant), using a coded party identifier.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+BY+1003::92."
    },
    "NAD+SF": {
        "explanation": "Identifies the ship-from party (qualifier SF), the location or supplier’s facility from which goods are dispatched.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+SF+SUPPLIER001::92."
    },
    "NAD+ST": {
        "explanation": "Identifies the ship-to party (qualifier ST), the destination (e.g., Volvo Cars plant or warehouse), using a coded party identifier.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+ST+BP2TD::92."
    },
    "LOC+11": {
        "explanation": "Specifies the place/port of discharge (qualifier 11), the primary delivery location (e.g., a Volvo Cars plant), using a coded location ID.",
        "usage": "Required (R, an..3 for qualifier; R, an..35 for location ID), Level 2, MaxOcc: 1. Example: LOC+11+TAV::92."
    },
    "NAD+CC": {
        "explanation": "Identifies the consolidation center (qualifier CC), an intermediate facility where goods are consolidated before final delivery.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+CC+CONSOL001::92."
    },
    "NAD+CA": {
        "explanation": "Identifies the carrier (qualifier CA), the transport company responsible for delivering the goods.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..35 for party ID), Level 1, MaxOcc: 1. Example: NAD+CA+CARRIER001::92."
    },
    "TDT+20": {
        "explanation": "Specifies main-carriage transport information (qualifier 20), including transport mode, carrier details, and vehicle information.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..17 for transport ID), Level 1, MaxOcc: 1. Example: TDT+20+++++CARRIER001::92."
    },
    "TDT+10": {
        "explanation": "Specifies pre-carriage transport information (qualifier 10), detailing initial transport from the supplier to a consolidation point or port.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..17 for transport ID), Level 1, MaxOcc: 1. Example: TDT+10+++++PRECAR001::92."
    },
    "CPS": {
        "explanation": "Specifies the consignment packing sequence, identifying the hierarchical level of packaging (e.g., pallet, box) within the despatch.",
        "usage": "Required (R, an..17 for hierarchical ID), Level 2, MaxOcc: 9999. Example: CPS+1. Note: Inferred from message structure (Page 2) and branching diagram (Page 4), as part of despatch control line."
    },
    "PAC": {
        "explanation": "Describes the number and type of packages (e.g., pallets, boxes) in the consignment, including package type codes.",
        "usage": "Required (R, n..8 for number of packages; R, an..17 for package type), Level 3, MaxOcc: 9999. Example: PAC+10++PAL. Note: Inferred from message structure (Page 2) and EDIFACT standard, as part of packaging details."
    },
    "LIN": {
        "explanation": "Identifies a specific item in the despatch using the buyer’s article number (Volvo Cars’ part number) from the DELFOR/DELJIT message.",
        "usage": "Required (R, an..35 for article number), Level 3, MaxOcc: 1. Example: LIN+++12345678:IN. Note: Inferred from branching diagram (Page 4) and EDIFACT standard, as part of part data."
    },
    "PIA": {
        "explanation": "Provides additional item identifiers (e.g., drawing revision, supplier’s part number) to clarify specifications beyond the LIN segment.",
        "usage": "Dependent (D, an..35 for additional ID), Level 4, MaxOcc: 10. Example: PIA+1+PO4:DR. Note: Inferred from message structure (Page 2) and EDIFACT standard, as part of part data."
    },
    "QTY+12": {
        "explanation": "Specifies the despatched quantity (qualifier 12) of the item identified in the LIN segment, indicating the number of units shipped.",
        "usage": "Required (R, an..3 for qualifier; R, n..15 for quantity), Level 4, MaxOcc: 1. Example: QTY+12:100. Note: Inferred from message structure (Page 2) and EDIFACT standard, as part of part data."
    },
    "QTY+113": {
        "explanation": "Specifies the scheduled quantity (qualifier 113) linked to the despatch, referencing quantities planned in the DELFOR/DELJIT message.",
        "usage": "Dependent (D, an..3 for qualifier; R, n..15 for quantity), Level 4, MaxOcc: 1. Example: QTY+113:100. Note: Inferred from EDIFACT standard and Volvo Cars’ context, distinguishing from QTY+12."
    },
    "RFF+CRN": {
        "explanation": "References the EUR 1 certificate number (qualifier CRN), used for customs purposes to certify the origin of goods.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..35 for reference number), Level 3, MaxOcc: 1. Example: RFF+CRN:EUR1202501001."
    },
    "LOC+159": {
        "explanation": "Specifies an additional internal destination (qualifier 159), an internal delivery point within the consignee’s facility (e.g., dock or gate), printed on the transport label.",
        "usage": "Dependent (D, an..3 for qualifier; R, an..12 for location ID), Level 3, MaxOcc: 1. Example: LOC+159+550-1C5A-Y25::92."
    },
    "UNT": {
        "explanation": "Closes the message with a segment count and repeats the UNH reference number for integrity.",
        "usage": "Mandatory (M, n..6 for segment count; M, an..14 for reference), Level 0, MaxOcc: 1. Example: UNT+48+XFR151560."
    },
    "UNZ": {
        "explanation": "The Interchange Trailer segment closes the interchange, specifying the number of messages and repeating the UNB control reference.",
        "usage": "Mandatory (M, n..6 for message count; M, an..14 for control reference), Interchange Level, MaxOcc: 1. Example: UNZ+1+000000001."
    }
}

def explain_segment(segment):
    segment_info = segment_explanations_d07a.get(segment.upper(), None)
    if segment_info:
        return f"**Explanation**\n{segment_info['explanation']}\n\n**Usage**\n{segment_info['usage']}"
    return f"No explanation available for DESADV D07A segment {segment}."

def process(user_message):
    """
    Process a user message using DESADV_D07A specification.
    
    Args:
        user_message (str): The user's input message (e.g., 'UNH' or 'What is the UNH segment?').
    
    Returns:
        str: The formatted explanation of the segment.
    """
    # Parse the message to extract a segment code
    words = user_message.upper().split()
    segment = next((word for word in words if word in segment_explanations_d07a), None)
    if segment:
        return explain_segment(segment)
    return f"Could not find a valid segment code in your message: {user_message}"