segment_explanations_d04a = {
    "UNB": {
        "explanation": "The Interchange Header segment (UNB) marks the beginning of an EDI interchange, which may contain one or more messages (e.g., DELFOR D04A). It defines the syntax rules, sender and recipient identification, date and time of preparation, and a unique interchange control reference. In the context of Volvo Cars’ DELFOR D04A, it ensures that the interchange is correctly routed and processed between plants and the supplier’s EDI systems.",
        "usage": "Mandatory segment (status not explicitly detailed in the document’s comparison table on Page 11, but standard for EDIFACT interchanges) used to initiate the EDI interchange. It includes:\n- Syntax Identifier: Specifies the EDIFACT syntax version (e.g., UNOA or UNOB).\n- Sender and Recipient IDs: Identifies Volvo Cars (sender) and the supplier (recipient) using agreed-upon codes (e.g., GLN or DUNS numbers).\n- Date and Time: Records when the interchange was prepared (format CCYYMMDD:HHMM).\n- Interchange Control Reference: A unique identifier for tracking the interchange.\nExample (based on EDIFACT standards, as not shown in the document’s message example): UNB+UNOA:4+SenderID:Qualifier+RecipientID:Qualifier+20230803:0501+000000001++DELFOR, where:\n- UNOA:4 indicates syntax version 4.\n- SenderID and RecipientID are Volvo Cars’ and supplier’s IDs.\n- 20230803:0501 is the preparation date/time (August 3, 2023, 05:01).\n- 000000001 is the control reference.\n- DELFOR indicates the message type.\nThe UNB segment is critical for establishing the communication framework, ensuring the DELFOR D04A message is delivered to the correct recipient and processed under the agreed EDI standards."
    },
    "UNH": {
        "explanation": "The Message Header segment identifies the start of the DELFOR D04A message, specifying a unique message reference number and message type (DELFOR, version D04A, UN/EDIFACT). It ensures the message is correctly processed by the recipient’s EDI system.",
        "usage": "Mandatory segment (M, an..14) used to initiate the message. For example, it includes the message reference number to track the message uniquely in PLANTS’ and suppliers’ systems."
    },
    "BGM": {
        "explanation": "The Beginning of Message segment defines the document type (code '241' for batch delivery schedule per Volvo Cars’ supply process) and includes the delivery schedule number. It also indicates the message function (e.g., original or replacement, code 5).",
        "usage": "Required (M, an..35 for document name; R, an..35 for schedule number) to specify the message’s purpose and identity. Example: BGM+241::BATCH+1000006440+5 identifies a batch delivery schedule with number 1000006440."
    },
    "DTM+137": {
        "explanation": "Specifies the date and time when the DELFOR document was created, using format CCYYMMDDHHMM. It establishes the message’s issuance timestamp.",
        "usage": "Required (R, an..35) for tracking when the schedule was generated. Example: DTM+137:202308030501:203 indicates creation on August 3, 2023, at 05:01."
    },
    "DTM+157": {
        "explanation": "Indicates the validity start date of the delivery schedule (format CCYYMMDD), marking when the schedule becomes effective.",
        "usage": "Required (R, an..35) to define the schedule’s start date. Example: DTM+157:20230803:102 sets validity from August 3, 2023."
    },
    "DTM+36": {
        "explanation": "Defines the expiry date of the delivery schedule (format CCYYMMDD), typically for short-term schedules, marking the end of the validity period.",
        "usage": "Required (R, an..35) to specify the schedule’s end date. Example: DTM+36:20240624:102 sets expiry on June 24, 2024."
    },
    "NAD+SE": {
        "explanation": "The Name and Address segment with qualifier SE (Seller) identifies the supplier (seller) involved in the delivery schedule. It uses a coded identifier (e.g., Volvo Cars’ partner ID) to ensure accurate identification of the supplier in the EDI transaction.",
        "usage": "Mandatory (M, an5) to specify the supplier’s identity. The coded ID is typically a standardized identifier like a GLN or a Volvo Cars-specific partner ID. Example: NAD+SE+B1234::92 identifies the supplier with partner ID B1234, using qualifier 92 (assigned by Volvo Cars). This information is critical for routing the DELFOR D04A message and coordinating with the correct supplier."
    },
    "NAD+BY": {
        "explanation": "The Name and Address segment with qualifier BY (Buyer) identifies the buyer, which in this context is typically a Volvo Cars entity (e.g., a purchasing unit or plant). It uses a coded identifier to ensure precise identification of the buyer in the supply chain.",
        "usage": "Mandatory (M, an5) to specify the buyer’s identity. The coded ID ensures clarity in transactions. Example: NAD+BY+BP2TD::92 identifies the buyer (e.g., Volvo Cars’ Torslanda plant) with partner ID BP2TD, using qualifier 92. This segment is essential for defining the entity issuing the delivery schedule."
    },
    "NAD+MF": {
        "explanation": "The Name and Address segment with qualifier MF (Manufacturer) identifies the manufacturing party responsible for producing the parts specified in the delivery schedule. This may be the same as the supplier or a distinct entity, depending on the supply chain structure. It uses a coded identifier for accuracy.",
        "usage": "Mandatory (M, an5) to specify the manufacturer’s identity. This segment is particularly relevant when the manufacturing entity differs from the supplier or ship-from location. Example: NAD+MF+B1234::92 identifies the manufacturer with partner ID B1234, using qualifier 92. It ensures traceability of the production source in Volvo Cars’ supply chain."
    },
    "NAD+SF": {
        "explanation": "The Name and Address segment with qualifier SF (Ship-From) identifies the location from which the parts are shipped, as specified in the purchase order. This is critical for logistics coordination and must be included in the supplier’s DESADV (Despatch Advice) message to confirm the shipping origin.",
        "usage": "Mandatory (M, an5) to specify the ship-from location. The coded ID aligns with the purchase order and is used for transport planning. Example: NAD+SF+B1234::92 identifies the ship-from location with partner ID B1234, using qualifier 92. This segment is vital for ensuring accurate pick-up and delivery logistics, especially when linked to Transport Order (TO) numbers in firm orders."
    },
    "GEI": {
        "explanation": "Processing Information segment indicates the level of delivery instruction details (code '3' for schedule dates and quantities for a specific ship-to party, e.g., a plant).",
        "usage": "Mandatory (M, an..3) to signal the message’s structural level. Example: GEI+3 denotes delivery instruction details for a plant."
    },
    "NAD+ST": {
        "explanation": "Specifies the Ship-To party (e.g., a Volvo Cars plant) with details like ID, short name, address, and full name. It identifies the delivery destination.",
        "usage": "Mandatory (M, an5 for ID; an..20 for short name/address; an..35 for name) to define the delivery location. Example: NAD+ST+BP2TD::92+VOLVO TORSLANDA KAROSS specifies the Torslanda plant."
    },
    "CTA": {
        "explanation": "Provides the name of the Supply Chain Coordinator (SCC) responsible for the ship-to location, facilitating direct communication.",
        "usage": "Required (R, an..35) to identify the coordinator. Example: CTA+MC+:Name Nameson names the coordinator."
    },
    "COM": {
        "explanation": "Contains the SCC’s contact details, including email (EM) and phone number (TE), for coordination and issue resolution.",
        "usage": "Mandatory (M, an..100) for contact information. Example: COM+name.nameson@volvocars.com:EM provides the email address."
    },
    "LIN": {
        "explanation": "Identifies the buyer’s article number (Volvo Cars’ part number) for the item in the delivery schedule.",
        "usage": "Required (R, an..35) to specify the part. Example: LIN++38+12345678:IN identifies part number 12345678."
    },
    "PIA": {
        "explanation": "Provides additional product identifiers, such as drawing revision number, commodity grouping, or customs HS code, to clarify part specifications.",
        "usage": "Optional (O, an..35) for extra details. Example: PIA+1+++PO4:DR specifies a drawing revision."
    },
    "IMD": {
        "explanation": "Contains Volvo Cars’ part description in English, aiding supplier understanding of the item.",
        "usage": "Required (R, an..35) for part description. Example: IMD+++::PART DESCRIPTION::ENG provides the description."
    },
    "MEA+WT+U": {
        "explanation": "Specifies the part’s weight per unit (in kilograms), critical for logistics and packaging planning.",
        "usage": "Mandatory (M, an..8) and required (R, an..18) for weight. Example: MEA+WT+U+KGM:2.693 indicates a unit weight of 2.693 kg."
    },
    "LOC+11/159": {
        "explanation": "Defines the place/port of discharge (LOC+11) and additional internal destination (LOC+159) within Volvo Cars’ facilities.",
        "usage": "Required (R, an..35) for delivery location details. Example: LOC+11+TAV::92 specifies the reception point."
    },
    "DTM+257": {
        "explanation": "Indicates the date and time when delivery quantities were calculated (format CCYYMMDDHHMM), which may differ from the document date.",
        "usage": "Required (R, an..35) for calculation timestamp. Example: DTM+257:202308030015:203 sets calculation time as August 3, 2023, 00:15."
    },
    "RFF+ON": {
        "explanation": "References the purchase order number associated with the delivery schedule.",
        "usage": "Required (R, an..35) to link to the order. Example: RFF+ON:111122222002 specifies the purchase order."
    },
    "RFF+AIF": {
        "explanation": "References the previous delivery schedule number, absent in the first schedule.",
        "usage": "Required (R, an..35) when applicable. Example: RFF+AIF:1000006412 links to the prior schedule."
    },
    "QTY+83": {
        "explanation": "Specifies the backorder quantity, i.e., ordered quantities not yet goods received.",
        "usage": "Mandatory (M, n..15) if backorders exist. Example: QTY+83:128 indicates 128 units on backorder."
    },
    "QTY+70": {
        "explanation": "Specifies the cumulative quantity of goods received since the date in DTM+51.",
        "usage": "Mandatory (M, n..15) for tracking received quantities. Example: QTY+70:9600 indicates 9600 units received."
    },
    "QTY+57": {
        "explanation": "Specifies the in-transit quantity, i.e., the sum of parts shipped (per ASN) but not yet goods received.",
        "usage": "Mandatory (M, n..15) if in-transit parts exist. Example: QTY+57:256 indicates 256 units in transit."
    },
    "DTM+51": {
        "explanation": "Specifies the start date for the cumulative quantity in QTY+70 (format CCYYMMDD).",
        "usage": "Required (R, an..35) for cumulative tracking. Example: DTM+51:20230101:102 sets the start date as January 1, 2023."
    },
    "QTY+12": {
        "explanation": "Specifies the despatched quantity according to the ASN for a specific delivery note.",
        "usage": "Mandatory (M, n..15) for delivery note details. Example: QTY+12:64 indicates 64 units despatched."
    },
    "QTY+48": {
        "explanation": "Specifies the quantity goods received for a specific delivery note.",
        "usage": "Mandatory (M, n..15) for received quantities. Example: QTY+48:64 indicates 64 units received."
    },
    "DTM+11": {
        "explanation": "Specifies the despatch date/time of the ASN (format CCYYMMDDHHMM) for a delivery note.",
        "usage": "Required (R, an..35) for despatch timing. Example: DTM+11:20230710:102 sets despatch date as July 10, 2023."
    },
    "DTM+50": {
        "explanation": "Specifies the goods receipt date (format CCYYMMDD) when the delivery note was received.",
        "usage": "Required (R, an..35) for receipt timing. Example: DTM+50:20230707:102 sets receipt date as July 7, 2023."
    },
    "RFF+AAK": {
        "explanation": "Specifies the despatch advice number (delivery note number) for goods received.",
        "usage": "Required (R, an..35) when delivery notes are goods received. Example: RFF+AAK:12345678 identifies a delivery note."
    },
    "SCC": {
        "explanation": "Specifies the commitment level of the schedule: code 1 (Firm) for confirmed quantities, code 4 (Forecast) for planning quantities, or code 9 (User-defined) with plant-specific instructions.",
        "usage": "Mandatory (M, an..3) to indicate order type. Example: SCC+1 denotes a firm order; SCC+4 denotes a forecast."
    },
    "QTY+113": {
        "explanation": "Specifies the quantity to be delivered on a given date, either firm or forecast.",
        "usage": "Mandatory (M, n..15) for delivery quantities. Example: QTY+113:64 indicates 64 units to be delivered."
    },
    "DTM+10": {
        "explanation": "Specifies the requested shipment date/time (format CCYYMMDDHHMM) for the quantity in QTY+113.",
        "usage": "Required (R, an..35) for delivery timing. Example: DTM+10:202308070800:203 sets shipment date as August 7, 2023, 08:00."
    },
    "RFF+AAO": {
        "explanation": "Specifies the Transport Order (TO) number from the Transport Management System (TMS) for firm orders, ensuring logistics coordination.",
        "usage": "Required (R, an..35) for firm orders with a TO. Example: RFF+AAO:FAA0001 identifies the TO number."
    },
    "PAC": {
        "explanation": "Specifies the type of packaging used for the delivery, critical for logistics planning.",
        "usage": "Required (R, an..17) for packaging details. Example: PAC++4+1280::92 specifies the packaging type."
    },
    "MEA+AAY": {
        "explanation": "Specifies package measurements, including net weight (AAL), length (LN), width (WD), and height (HT), in units like kilograms and millimeters.",
        "usage": "Required (R, an..18) for packaging dimensions. Example: MEA+AAY+AAL+KGM:195 indicates a net weight of 195 kg."
    },
    "QTY+52": {
        "explanation": "Specifies the quantity per pack (unit load quantity) in the load carrier defined in the PAC segment.",
        "usage": "Mandatory (M, n..15) for packaging quantity. Example: QTY+52:2.1 indicates 2.1 units per pack."
    },
    "DTM+7": {
        "explanation": "Specifies the date from which the packaging instruction is valid (format CCYYMMDD).",
        "usage": "Required (R, an..35) for packaging validity. Example: DTM+7:20230803:102 sets validity from August 3, 2023."
    }
}

def explain_segment(segment):
    segment_info = segment_explanations_d04a.get(segment.upper(), None)
    if segment_info:
        return f"**Explanation**\n{segment_info['explanation']}\n\n**Usage**\n{segment_info['usage']}"
    return f"No explanation available for DELFOR D04A segment {segment}."

def process(user_message):
    """
    Process a user message using DELFOR_D04A specification.
    
    Args:
        user_message (str): The user's input message (e.g., 'UNH' or 'What is the UNH segment?').
    
    Returns:
        str: The formatted explanation of the segment.
    """
    # Parse the message to extract a segment code
    words = user_message.upper().split()
    segment = next((word for word in words if word in segment_explanations_d04a), None)
    if segment:
        return explain_segment(segment)
    return f"Could not find a valid segment code in your message: {user_message}"