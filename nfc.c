#include <stdlib.h>
#include <string.h>
#include <nfc/nfc.h>


static void
get_hex(char* str, const uint8_t *pbtData, const size_t szBytes)
{
  size_t  szPos;
  char temp[20];
  for (szPos = 0; szPos < szBytes; szPos++) {
    sprintf(str,"%02d", pbtData[szPos]);
    strcat(temp,str);
  }  
sprintf(str,temp);
}


int main(int argc, const char *argv[]){
  
  nfc_device *pnd;
  nfc_target nt;
  nfc_context *context;

  nfc_init(&context);
  if (context == NULL) {
    printf("Unable to init libnfc (malloc)\n");
    exit(EXIT_FAILURE);
  }

  pnd = nfc_open(context, NULL);
  if (pnd == NULL) {
    printf("ERROR: %s\n", "Unable to open NFC device.");
    exit(EXIT_FAILURE);
  }
  if (nfc_initiator_init(pnd) < 0) {
    nfc_perror(pnd, "nfc_initiator_init");
    exit(EXIT_FAILURE);
  }

  int uid = 0;
  char str[20];
  const nfc_modulation nmMifare = {
    .nmt = NMT_ISO14443A,
    .nbr = NBR_106,
  };
  if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
    get_hex(str, nt.nti.nai.abtUid, nt.nti.nai.szUidLen);
  }
  
  nfc_close(pnd);
  nfc_exit(context);
  sscanf(str, "%8d", &uid);
  return uid;
}
