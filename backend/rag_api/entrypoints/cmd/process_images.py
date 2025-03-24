from cloudevents.http import CloudEvent
import functions_framework
from google.events.cloud import firestore
from rag_api.infrastructure.bindings import di
from rag_api.infrastructure.ports import LLMPort, VectorDBPort, RequirementsStorePort
import os
from dotenv import load_dotenv

load_dotenv()

# @functions_framework.cloud_event
# def main(cloud_event: CloudEvent) -> None:
#     """Triggers by a change to a Firestore document.

#     Args:
#         cloud_event: cloud event with information on the firestore event trigger
#     """
#     firestore_payload = firestore.DocumentEventData()
#     firestore_payload._pb.ParseFromString(cloud_event.data)

#     print(f"Function triggered by change to: {cloud_event['source']}")

#     print("\nOld value*******:")
#     print(firestore_payload.old_value)

#     print("\nNew value*****:")
#     print(firestore_payload.value)


def process_images(requirements_service: RequirementsStorePort, vector_db: VectorDBPort, llm_service: LLMPort):
    try:
        print("Reading from Firestore")
        for doc in vector_db.iterate_documents():
            print(f"Processing document: {doc.to_dict()['ticket_id']}")
            document = doc.to_dict()
            image = requirements_service.download_attachment(url=document["images"][0]) if "images" in document and len(document["images"]) > 0 else None
            if image:
                answers = llm_service.ask_question_on_image(image_loc=image, image_bytes=image, question="What is in this image?")
                print(f"Answers: {answers}")
                vector_db.update_document_with_additional_info(document_id=doc.id, additional_info=answers)
            else:
                print("No image found")
        print(f"message: Image processing successful")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
   process_images(di["AzureRequirements"], di["FirestoreVectorDB"], di["GoogleGenAILLM"])