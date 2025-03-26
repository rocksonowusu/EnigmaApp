from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .enigma_logic import ROTORS, EnigmaMachine
from .models import EncryptionHistory  # Import the model


class EnigmaEncryptView(APIView):
    def post(self, request):
        """Encrypts a message using the Enigma machine and stores it in the database"""
        try:
            message = request.data.get("message", "").upper()
            rotor_settings = request.data.get("rotor_settings", [])  # Retrieve rotor settings properly
            
            # Validate rotor settings (must be integers or digits as strings)
            if not all(isinstance(i, int) or (isinstance(i, str) and i.isdigit()) for i in rotor_settings):
                return Response({"error": "Rotor settings must be integers."}, status=status.HTTP_400_BAD_REQUEST)

            rotor_settings = [int(i) for i in rotor_settings]  # Convert all to integers

            # Check if the rotor settings are within the allowed range
            if any(r < 0 or r >= len(ROTORS) for r in rotor_settings):
                return Response({"error": f"Rotor settings must be between 0 and {len(ROTORS) - 1}."}, status=status.HTTP_400_BAD_REQUEST)

            plugboard_settings = request.data.get("plugboard_settings", {})

            # Encrypt the message
            enigma = EnigmaMachine(rotor_settings, plugboard=plugboard_settings)
            encrypted_message = enigma.encrypt_message(message)

            # Save to the database
            encryption_record = EncryptionHistory.objects.create(
                message=message,
                encrypted_message=encrypted_message,
                rotor_settings=rotor_settings,
                plugboard_settings=plugboard_settings
            )

            return Response(
                {
                    "id": encryption_record.id,  # Return the record ID
                    "encrypted_message": encrypted_message,
                    "timestamp": encryption_record.timestamp,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EnigmaDecryptView(APIView):
    def post(self, request):
        """Decrypts a message using the Enigma machine (same as encryption)"""
        try:
            encrypted_message = request.data.get("encrypted_message", "").upper()
            rotor_settings = request.data.get("rotor_settings", [])

            if not all(isinstance(i, int) or (isinstance(i, str) and i.isdigit()) for i in rotor_settings):
                return Response({"error": "Rotor settings must be integers."}, status=status.HTTP_400_BAD_REQUEST)

            rotor_settings = [int(i) for i in rotor_settings]

            if any(r < 0 or r >= len(ROTORS) for r in rotor_settings):
                return Response({"error": f"Rotor settings must be between 0 and {len(ROTORS) - 1}."}, status=status.HTTP_400_BAD_REQUEST)

            plugboard_settings = request.data.get("plugboard_settings", {})

            # Decrypt (Enigma decryption is the same as encryption)
            enigma = EnigmaMachine(rotor_settings, plugboard=plugboard_settings)
            decrypted_message = enigma.encrypt_message(encrypted_message)

            return Response({"decrypted_message": decrypted_message}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EncryptionHistoryView(APIView):
    """Fetches past encryption records"""
    def get(self, request):
        records = EncryptionHistory.objects.all().order_by("-timestamp")
        data = [
            {
                "id": record.id,
                "message": record.message,
                "encrypted_message": record.encrypted_message,
                "rotor_settings": record.rotor_settings,
                "plugboard_settings": record.plugboard_settings,
                "timestamp": record.timestamp,
            }
            for record in records
        ]
        return Response(data, status=status.HTTP_200_OK)
