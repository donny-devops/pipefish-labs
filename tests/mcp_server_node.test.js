/**
 * PipeFish Labs — Node.js MCP Server Test Suite
 * Runner: node:test / node:assert
 */

import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { handleMcpMessage, TOOLS, AGENT_REGISTRY } from '../bin/mcp-server.js';

describe('Node.js MCP Server Protocol & Tools Verification', () => {
  test('initialize handshake returns MCP 2024-11-05 protocol version and capabilities', () => {
    const resp = handleMcpMessage({
      jsonrpc: '2.0',
      id: 'init-1',
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {}
      }
    });

    assert.equal(resp.jsonrpc, '2.0');
    assert.equal(resp.id, 'init-1');
    assert.equal(resp.result.protocolVersion, '2024-11-05');
    assert.equal(resp.result.serverInfo.name, 'pipefish-labs-mcp-server');
    assert.equal(resp.result.serverInfo.version, '2.4.0');
  });

  test('tools/list returns exactly 9 registered MCP tools with schemas', () => {
    const resp = handleMcpMessage({
      jsonrpc: '2.0',
      id: 'tools-list-1',
      method: 'tools/list',
      params: {}
    });

    assert.equal(resp.id, 'tools-list-1');
    assert.equal(resp.result.tools.length, 9);

    const toolNames = resp.result.tools.map((t) => t.name);
    assert.ok(toolNames.includes('trigger_agent_graph'));
    assert.ok(toolNames.includes('get_agent_spec'));
    assert.ok(toolNames.includes('verify_enclave_status'));
    assert.ok(toolNames.includes('k8s_autoscale_check'));
    assert.ok(toolNames.includes('vault_lease_issue'));
    assert.ok(toolNames.includes('ebpf_kernel_profile'));
    assert.ok(toolNames.includes('db_zdr_query'));
    assert.ok(toolNames.includes('llmops_eval_run'));
    assert.ok(toolNames.includes('list_agents'));
  });

  test('tools/call list_agents returns all 26 agents', () => {
    const resp = handleMcpMessage({
      jsonrpc: '2.0',
      id: 'call-list-1',
      method: 'tools/call',
      params: {
        name: 'list_agents',
        arguments: {}
      }
    });

    assert.equal(resp.id, 'call-list-1');
    const content = JSON.parse(resp.result.content[0].text);
    assert.equal(content.total_agents, 26);
    assert.equal(content.agents.length, 26);
  });

  test('tools/call trigger_agent_graph executes 8-node DAG with ZDR', () => {
    const resp = handleMcpMessage({
      jsonrpc: '2.0',
      id: 'call-trigger-1',
      method: 'tools/call',
      params: {
        name: 'trigger_agent_graph',
        arguments: {
          scenario_key: 'missedcalltextback',
          payload: { caller: '+14155550199', priority: 'high' }
        }
      }
    });

    assert.equal(resp.id, 'call-trigger-1');
    const content = JSON.parse(resp.result.content[0].text);
    assert.equal(content.status, 'COMPLETED');
    assert.equal(content.nodes_executed, 8);
    assert.equal(content.zdr_retention_bytes, 0);
    assert.equal(content.scenario, 'missedcalltextback');
  });

  test('tools/call llmops_eval_run evaluates prompts and canary drift', () => {
    const resp = handleMcpMessage({
      jsonrpc: '2.0',
      id: 'call-llmops-1',
      method: 'tools/call',
      params: {
        name: 'llmops_eval_run',
        arguments: {
          prompt_template: 'customer_support_intake_v2',
          models: ['gemini-2.5-flash', 'claude-3-7-sonnet']
        }
      }
    });

    assert.equal(resp.id, 'call-llmops-1');
    const content = JSON.parse(resp.result.content[0].text);
    assert.equal(content.status, 'COMPLETED');
    assert.equal(content.benchmark_results.length, 2);
    assert.equal(content.benchmark_results[0].canary_ready, true);
  });
});
