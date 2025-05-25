segment_explanations_d96a = {
    "UNB": {
        "explanation": "The Interchange Header segment defines the interchange’s metadata, identifying the sender and recipient (using identifiers like GLN or DUNS), date/time of preparation, and a unique interchange control reference. It specifies the syntax rules (e.g., UNOC character set) and the application reference (e.g., DELFOR) for processing the interchange, which may contain multiple messages like DELFOR.",
        "usage": "Mandatory (M, an..4 for syntax identifier; M, an..35 for sender/recipient IDs; M, an..14 for control reference), Interchange Level (outside message structure), MaxOcc: 1. Example: UNB+UNOC:3+1234567890123:14+9876543210987:14+150301:1000+000000001++DELFOR. Note: Not explicitly detailed in the provided document, but standard for EDIFACT interchanges, likely used by Volvo Cars to route DELFOR messages to suppliers."
    },
    "UNH": {
        "explanation": "Marks the start of the DELFOR D96A message with a unique reference number, message type (DELFOR), version (D), release (96A), controlling agency (UN), and association code (A09040).",
        "usage": "Mandatory (M, an..14 for reference number; M, an..6 for message type), Level 0, MaxOcc: 1. Example: UNH+1144295+DELFOR:D:96A:UN:A09040."
    },
    "BGM": {
        "explanation": "Defines the document as a batch delivery schedule (code 241), assigns a unique schedule number, and specifies the message function (e.g., 5 for replacement, 9 for original).",
        "usage": "Mandatory (M, an..3 for document code; R, an..35 for schedule number), Level 0, MaxOcc: 1. Example: BGM+241+1000006440+5."
    },
    "DTM+137": {
        "explanation": "Specifies the document/message creation date/time (qualifier 137) in CCYYMMDD (102) or CCYYMMDDHHMM (203) format, indicating when the DELFOR was issued.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..12 for date), Level 1, MaxOcc: 3. Example: DTM+137:20150301:102."
    },
    "DTM+157": {
        "explanation": "Specifies the validity start date (qualifier 157) in CCYYMMDD (102) format, indicating when the delivery schedule becomes effective.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..12 for date), Level 1, MaxOcc: 3. Example: DTM+157:20150305:102."
    },
    "DTM+36": {
        "explanation": "Specifies the expiry date (qualifier 36) in CCYYMMDD (102) format, indicating when the delivery schedule expires, often used for short-term DELFORs.",
        "usage": "Mandatory (M, an..3 for qualifier; R, an..12 for date), Level 1, MaxOcc: 3. Example: DTM+36:20150415:102."
    },
    "NAD+BY": {
        "explanation": "Identifies the buyer (qualifier BY), typically a Volvo Cars entity (e.g., purchasing unit or plant), using a coded party identifier.",
        "usage": "Mandatory (M, an..3 for qualifier; M, an..20 for party ID), Level 1, MaxOcc: 1. Example: NAD+BY+1003::91."
    },
    "NAD+SE": {
        "explanation": "Identifies the seller (qualifier SE), the supplier providing parts or services, using a coded party identifier.",
        "usage": "Mandatory (M, an..3 for qualifier; M, an..20 for party ID), Level 1, MaxOcc: 1. Example: NAD+SE+2003::91."
    },
    "NAD+CN": {
        "explanation": "Identifies the consignee (qualifier CN), the delivery destination (e.g., a Volvo Cars plant or warehouse), using a coded party identifier.",
        "usage": "Mandatory (M, an..3 for qualifier; M, an..20 for party ID), Level 1, MaxOcc: 1, Conditional. Example: NAD+CN+BP2TD::91."
    },
    "UNS": {
        "explanation": "Separates the header from the detail section using code 'S' to indicate the detail/summary transition.",
        "usage": "Mandatory (M, a1 for section ID), Level 0, MaxOcc: 1. Example: UNS+S."
    },
    "LIN": {
        "explanation": "Identifies a part in the schedule using the buyer’s article number (Volvo Cars’ part number).",
        "usage": "Mandatory (M, an..35 for article number), Level 2, MaxOcc: 9999. Example: LIN+++12345678:IN."
    },
    "PIA": {
        "explanation": "Provides additional part identifiers (e.g., drawing revision, commodity code) to clarify specifications beyond the LIN segment.",
        "usage": "Conditional (C, an..35 for additional ID), Level 3, MaxOcc: 10. Example: PIA+1+PO4:DR."
    },
    "LOC+11": {
        "explanation": "Specifies the place/port of discharge (qualifier 11), the primary delivery location (e.g., a Volvo Cars plant), using a coded location ID.",
        "usage": "Required (R, an..35 for location code), Level 3, MaxOcc: 100. Example: LOC+11+TAV::91."
    },
    "LOC+159": {
        "explanation": "Specifies an additional internal destination (qualifier 159), an internal delivery point within the consignee’s facility (e.g., a specific dock or storage area).",
        "usage": "Required (R, an..35 for location code), Level 3, MaxOcc: 100. Example: LOC+159+DOCK1::91."
    },
    "DTM+257": {
        "explanation": "Specifies the calculation date/time (qualifier 257) in CCYYMMDDHHMM (203) format, indicating when delivery quantities were calculated.",
        "usage": "Conditional (C, an..35 for date), Level 3, MaxOcc: 1. Example: DTM+257:201503010015:203."
    },
    "DTM+51": {
        "explanation": "Specifies the cumulative quantity start date (qualifier 51) in CCYYMMDD (102) format, setting the baseline for tracking cumulative quantities.",
        "usage": "Conditional (C, an..35 for date), Level 3, MaxOcc: 1. Example: DTM+51:20150101:102."
    },
    "RFF+ON": {
        "explanation": "References a purchase order (qualifier ON), linking the delivery schedule to a specific order.",
        "usage": "Mandatory (M, an..35 for reference number), Level 3, MaxOcc: 1. Example: RFF+ON:111122222002."
    },
    "RFF+AIF": {
        "explanation": "References a previous delivery instruction (qualifier AIF), identifying the prior schedule for updates or replacements.",
        "usage": "Mandatory (M, an..35 for reference number), Level 3, MaxOcc: 1. Example: RFF+AIF:1000006412."
    },
    "QTY+70": {
        "explanation": "Specifies the cumulative quantity (qualifier 70) of parts received since the DTM+51 date, tracking total goods received.",
        "usage": "Mandatory (M, n..15 for quantity), Level 3, MaxOcc: 1. Example: QTY+70:9600."
    },
    "QTY+113": {
        "explanation": "Specifies the outstanding or scheduled quantity (qualifier 113), either the total ordered quantity not yet delivered or the quantity to be delivered on a specific date (linked to DTM+10), representing firm or forecast requirements.",
        "usage": "Mandatory (M, n..15 for quantity), Level 3, MaxOcc: 1 (for outstanding), MaxOcc: 200 (for scheduled). Example: QTY+113:500 (outstanding); QTY+113:64 (scheduled)."
    },
    "QTY+83": {
        "explanation": "Specifies the backorder quantity (qualifier 83), ordered quantities not yet shipped or received, highlighting shortages.",
        "usage": "Mandatory (M, n..15 for quantity), Level 3, MaxOcc: 1. Example: QTY+83:128."
    },
    "QTY+12": {
        "explanation": "Specifies the despatched quantity (qualifier 12) from previous despatch notes (ASNs), tracking shipped quantities.",
        "usage": "Mandatory (M, n..15 for quantity), Level 3, MaxOcc: 200. Example: QTY+12:64."
    },
    "QTY+48": {
        "explanation": "Specifies the received quantity (qualifier 48) from previous despatch notes, tracking quantities received by the buyer.",
        "usage": "Mandatory (M, n..15 for quantity), Level 3, MaxOcc: 200. Example: QTY+48:64."
    },
    "RFF+AAK": {
        "explanation": "References a despatch advice (qualifier AAK), identifying the despatch note (ASN) associated with QTY+12/48 quantities.",
        "usage": "Mandatory (M, an..35 for reference number), Level 4, MaxOcc: 1. Example: RFF+AAK:12345678."
    },
    "DTM+11": {
        "explanation": "Specifies the despatch date (qualifier 11) in CCYYMMDD (102) format for quantities in QTY+12, indicating when goods were shipped.",
        "usage": "Conditional (C, an..35 for date), Level 5, MaxOcc: 1. Example: DTM+11:20150310:102."
    },
    "DTM+50": {
        "explanation": "Specifies the goods receipt date (qualifier 50) in CCYYMMDD (102) format for quantities in QTY+48, indicating when goods were received.",
        "usage": "Conditional (C, an..35 for date), Level 5, MaxOcc: 1. Example: DTM+50:20150312:102."
    },
    "SCC": {
        "explanation": "Defines the commitment level of scheduled quantities: Firm (1) or Planning/Forecast (4).",
        "usage": "Conditional (C, an..3 for condition code), Level 4, MaxOcc: 1. Example: SCC+1, SCC+4."
    },
    "DTM+10": {
        "explanation": "Specifies the requested shipment date/time (qualifier 10) in CCYYMMDDHHMM (203) format for the scheduled quantity in QTY+113.",
        "usage": "Conditional (C, an..35 for date), Level 4, MaxOcc: 2. Example: DTM+10:201503070800:203."
    },
    "RFF+AAO": {
        "explanation": "References a transport order (qualifier AAO) for scheduled quantities, ensuring logistics coordination.",
        "usage": "Mandatory (M, an..35 for reference number), Level 4, MaxOcc: 1. Example: RFF+AAO:FAA0001."
    },
    "UNT": {
        "explanation": "Closes the message with a segment count and repeats the UNH reference number for integrity.",
        "usage": "Mandatory (M, n..10 for segment count; M, an..14 for reference), Level 0, MaxOcc: 1. Example: UNT+25+1144295."
    }
}

def explain_segment(segment):
    segment_info = segment_explanations_d96a.get(segment.upper(), None)
    if segment_info:
        return f"**Explanation**\n{segment_info['explanation']}\n\n**Usage**\n{segment_info['usage']}"
    return f"No explanation available for DELFOR D96A segment {segment}."

def process(user_message):
    """
    Process a user message using DELFOR_D96A specification.
    
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