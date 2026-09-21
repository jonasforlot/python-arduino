// ============================================================
// DETECTEUR DE BRUIT - VERSION 8
// Arduino Nano 33 IoT + GT1146
//
// GT1146 D0 -> D4
// LED rouge -> D2 + résistance
// Buzzer -> D3
//
// PRINCIPE
// ------------------------------------------------------------
// D0 HIGH permanent       -> détection
// D0 HIGH/LOW alterné     -> détection
// D0 LOW permanent        -> calme
//
// FONCTIONNEMENT
// ------------------------------------------------------------
// 1. Détection pendant 2 s
// 2. LED rouge clignote pendant cette période
// 3. Puis buzzer pendant 1 s
// 4. Silence pendant 5 s
// 5. Nouveau bip si la détection continue
// 6. Retour au calme -> remise à zéro
// ============================================================


// ------------------------------------------------------------
// BROCHES
// ------------------------------------------------------------

const int GT1146  = 4;
const int LED    = 2;
const int BUZZER = 3;


// ------------------------------------------------------------
// REGLAGES
// ------------------------------------------------------------

const unsigned long TEMPS_AVANT_BIP = 2000;  // 2 secondes
const unsigned long DUREE_BIP       = 1000;  // 1 seconde
const unsigned long TEMPS_SILENCE   = 5000;  // 5 secondes

const unsigned long PERIODE_LED     = 500;  // clignotement


// ------------------------------------------------------------
// VARIABLES
// ------------------------------------------------------------

bool detection = false;
bool buzzerEnCours = false;

unsigned long debutDetection = 0;
unsigned long debutBuzzer = 0;
unsigned long prochainBip = 0;

unsigned long dernierChangement = 0;

bool etatLED = false;
unsigned long dernierClignotement = 0;


// ============================================================
// SETUP
// ============================================================

void setup() {

  pinMode(GT1146, INPUT);
  pinMode(LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);

  digitalWrite(LED, LOW);
  digitalWrite(BUZZER, LOW);

  Serial.begin(9600);

  delay(500);

  Serial.println();
  Serial.println("==============================");
  Serial.println(" DETECTEUR DE BRUIT - V8");
  Serial.println("==============================");
}


// ============================================================
// LOOP
// ============================================================

void loop() {

  unsigned long maintenant = millis();

  int etat = digitalRead(GT1146);


  // ==========================================================
  // 1. AFFICHAGE DU SIGNAL
  // ==========================================================

  Serial.println(etat == HIGH ? "D0 = HIGH" : "D0 = LOW");


  // ==========================================================
  // 2. DETECTION
  // ==========================================================

  // HIGH = signal de détection
  //
  // Peu importe que HIGH soit permanent ou qu'il alterne
  // avec LOW : dès qu'on observe HIGH, on considère qu'il
  // y a une activité sonore.

  if (etat == HIGH) {

    dernierChangement = maintenant;

    // Première détection
    if (!detection) {

      detection = true;
      debutDetection = maintenant;

      Serial.println(">>> DEBUT DETECTION");
    }
  }


  // ==========================================================
  // 3. RETOUR AU CALME
  // ==========================================================

  // Si D0 reste LOW pendant 1 seconde,
  // on considère que le bruit est terminé.

  if (detection &&
      etat == LOW &&
      maintenant - dernierChangement >= 1000) {

    detection = false;

    buzzerEnCours = false;

    debutDetection = 0;
    prochainBip = 0;

    digitalWrite(BUZZER, LOW);

    etatLED = false;
    digitalWrite(LED, LOW);

    Serial.println(">>> RETOUR AU CALME");
  }


  // ==========================================================
  // 4. PREMIERE ALERTE : LED
  // ==========================================================

  if (detection) {

    // La LED clignote immédiatement dès la détection

    if (maintenant - dernierClignotement >= PERIODE_LED) {

      dernierClignotement = maintenant;

      etatLED = !etatLED;

      digitalWrite(LED, etatLED);
    }
  }


  // ==========================================================
  // 5. DECLENCHEMENT DU BUZZER
  // ==========================================================

  // Le buzzer n'arrive qu'après 2 secondes de détection.

  if (detection &&
      !buzzerEnCours &&
      maintenant - debutDetection >= TEMPS_AVANT_BIP &&
      maintenant >= prochainBip) {

    buzzerEnCours = true;

    debutBuzzer = maintenant;

    digitalWrite(BUZZER, HIGH);

    Serial.println(">>> BIP !");
  }


  // ==========================================================
  // 6. FIN DU BIP
  // ==========================================================

  if (buzzerEnCours &&
      maintenant - debutBuzzer >= DUREE_BIP) {

    digitalWrite(BUZZER, LOW);

    buzzerEnCours = false;

    prochainBip = maintenant + TEMPS_SILENCE;

    Serial.println(">>> FIN BIP - silence 5 s");
  }


  delay(50);
}
