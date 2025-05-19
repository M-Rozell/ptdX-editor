from .colors import cprint, COLORS
import logging
logger = logging.getLogger(__name__)
logger.info("Update complete.")
logger.warning("Missing <Owner> tag.")
logger.error("Failed to parse XML file.")


# Update ptdX files from form Inputs
def update_elements(parent_element, parent_tag, updates):
    """Updates specific XML elements inside <A_002> and <I_002> or <A_003> and <I_003>."""
    parent = parent_element.find(parent_tag)
    updated = False

    # Define the elements that we need to update
    elements_to_update = [
        "Owner", "City", "Pipe_Use",  # Inside <A_002> or <A_003>
        "Customer", "Project", "WorkOrder", "Purpose"  # Inside <I_002> or <I_003>
    ]

    if parent is not None:
        for key in elements_to_update:
            if key in updates:  # Only update if the key is in the updates dictionary
                element = parent.find(key)
                if element is not None:
                    logger.info(f"Setting {key} to {updates[key]}")
                    #cprint(f"Setting {key} to {updates[key]}", COLORS["green"])  # Log the update
                    element.text = updates[key]  # Update the element value
                    updated = True
                else:
                        print(f"No element found for {key} inside {parent_tag}")


    return updated