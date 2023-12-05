"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runResolveBuildEnvironment = void 0;
const codeql_1 = require("./codeql");
const languages_1 = require("./languages");
const util = __importStar(require("./util"));
async function runResolveBuildEnvironment(cmd, logger, workingDir, languageInput) {
    logger.startGroup(`Attempting to resolve build environment for ${languageInput}`);
    const codeql = await (0, codeql_1.getCodeQL)(cmd);
    let language = languageInput;
    // If the CodeQL CLI version in use supports language aliasing, give the CLI the raw language
    // input. Otherwise, parse the language input and give the CLI the parsed language.
    if (!(await util.codeQlVersionAbove(codeql, codeql_1.CODEQL_VERSION_LANGUAGE_ALIASING))) {
        const parsedLanguage = (0, languages_1.parseLanguage)(languageInput)?.toString();
        if (parsedLanguage === undefined) {
            throw new util.UserError(`Did not recognize the language '${languageInput}'.`);
        }
        language = parsedLanguage;
    }
    let result = {};
    // If the CodeQL version in use does not support the `resolve build-environment`
    // command, just return an empty configuration. Otherwise invoke the CLI.
    if (!(await util.codeQlVersionAbove(codeql, codeql_1.CODEQL_VERSION_RESOLVE_ENVIRONMENT))) {
        logger.warning("Unsupported CodeQL CLI version for `resolve build-environment` command, " +
            "returning an empty configuration.");
    }
    else {
        if (workingDir !== undefined) {
            logger.info(`Using ${workingDir} as the working directory.`);
        }
        result = await codeql.resolveBuildEnvironment(workingDir, language);
    }
    logger.endGroup();
    return result;
}
exports.runResolveBuildEnvironment = runResolveBuildEnvironment;
//# sourceMappingURL=resolve-environment.js.map