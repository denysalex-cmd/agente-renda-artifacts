# Nitrosend Safe Mode MAP approval run

- **Environment and exact tooling.** Windows 10; Node.js `v24.22.0`; Nitrosend CLI `0.3.9`; `mailschema` `0.3.2`. I installed the validation package with `npm install --prefix tool --no-save mailschema@0.3.2`. The saved approval email was processed locally; no API key, token, password, or account credential is included here.

- **API-key execution path and hold.** The Nitrosend CLI profile reported `auth: api_key`. I used the API-key MCP surface to create/resolve the self-addressed contact with `nitro_manage_audience`, create a one-contact list, compose the campaign through `nitro_compose_campaign` (`intent` followed by the returned `generate` contract), review it with `nitro_review_delivery`, approve the draft for delivery, and request `live` with `nitro_control_delivery`. The send was held by Safe Mode at `2026-10-30T09:46:27Z`; it did not send until the account-owner decision.

- **Timing.** Safe Mode was already enabled before the API-key run. The first durable post-toggle API-key event is `2026-10-30T09:44:39Z`; the account-owner decision was recorded at `2026-10-30T10:07:07Z`, so the measured lower bound from confirmed Safe Mode operation to decision is **22 minutes 28 seconds**. The account history available to me does not expose the earlier toggle timestamp, so I did not invent a more precise value.

- **MAP extraction command.** I extracted the machine-readable part exactly as carried by the saved email with `npx -y mailschema@0.3.2 message approval.eml > description.json 2> message.stderr`. The tool reported `Valid MAP 0.3 description urn:uuid:6195e744-0014-5776-a8e0-c4a4a38acf05` and description digest `sha-256:581797e709532813d451c921a355b15415deb9f090a0c559ffa8188a64624084`.

- **Contract validation command and exact output.** I fetched `campaign-send-approval-0.1.json` from `https://mailschema.org/artifacts/map-0.3/contracts/campaign-send-approval-0.1.json` and ran `npx -y mailschema@0.3.2 description description.json --contract campaign-send-approval-0.1.json`. Exact stdout was:
  ```text
  Valid MAP 0.3 description urn:uuid:6195e744-0014-5776-a8e0-c4a4a38acf05
  sha-256:581797e709532813d451c921a355b15415deb9f090a0c559ffa8188a64624084
  ```

- **`terms.version` recomputation.** I loaded the extracted JSON, saved `description.terms.version`, deleted only `description.terms.version`, and passed the remaining object to `digest()` from `mailschema@0.3.2`: `node --input-type=module -e "import fs from 'node:fs'; import {digest} from './tool/node_modules/mailschema/dist/index.js'; const d=JSON.parse(fs.readFileSync('description.json','utf8')); const declared=d.terms.version; delete d.terms.version; const recomputed=digest(d); console.log(JSON.stringify({declared,recomputed,match:declared===recomputed}));"`. Declared and recomputed values were both `sha-256:b4fd18f4b9b245ddd6a610bce2059c4800b06b3d7fbf9209d81ceea7a62c4a94`; `match` was `true`.

- **Decision.** I chose **approve**. The MAP description matched the controlled request I intended: the expected sender, one self-addressed recipient, the reviewed content revision, and immediate delivery terms. Contract validation passed and the independently recomputed `terms.version` matched before the decision. Nitrosend recorded the approval at `2026-10-30T10:07:07Z`; the campaign completed at `2026-10-30T10:07:11Z` with one message sent and zero failures.

- **Slowest step.** The most time-consuming part was establishing the correct API-key CLI surface on Windows. A direct call to `nitro_create_contact` returned `tool_unavailable` with `This account cannot use nitro_create_contact.` and instructed me to run `nitrosend mcp tools list`. The available API-key catalog exposed contact/list creation through `nitro_manage_audience`; switching to that tool succeeded.

- **Defect/doc-gap check.** I found no MAP correctness defect after exercising saved-email extraction, Campaign Send Approval 0.1 validation, RFC 8785 digest binding, Safe Mode hold, human decision, and post-decision delivery. The reproducible surface friction above is worth documenting because the standalone contact tool name and the account-specific CLI catalog differ; `nitrosend mcp tools list --machine` is the reliable discovery step before assuming a tool name.

- **One change I would make.** Add the Safe Mode toggle time to account history or the approval resource. The send request and decision have precise timestamps, but the account history I queried did not expose the `safe_mode_enabled` transition, which makes an otherwise auditable toggle-to-decision duration depend on an external timestamp.